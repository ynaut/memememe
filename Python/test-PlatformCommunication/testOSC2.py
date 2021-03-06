from liblo import *
import sys
from time import sleep,time
from random import random
import math
sys.path.append("..")
from ax12 import ax12

class MyServer(ServerThread):
    def __init__(self):
        ServerThread.__init__(self, 8888)

    @make_method('/angles', 'ffffff')
    def foo_callback(self, path, args):
        #print args
        #print map(lambda x:math.degrees(x),args)
        anglesData.append(args)

def moveMotors():
    #print "wrinting on the motors..."
    angles = anglesData[0]

    del anglesData[0]

    anglesInt = []
    for (i,v) in enumerate(angles):
        angRadians = math.degrees(v)
        angInt = int(angRadians*1024/300)
        angPos = 520 + angInt
        angPos = 820 if angPos > 820 else angPos
        angPos = 220 if angPos < 220 else angPos
        anglesInt.append(angPos)
        angPos = angPos if (i+1)%2==0 else 1024-angPos
        try:
            servos.moveSpeedRW(i+1,angPos,1023)
        except:
            try:
                servos.moveSpeedRW(i+1,angPos,1023)
            except:
                print "3rd time c.p."
                pass

    servos.action()


def initMotors():
    global servos

    servos = ax12.Ax12()
    p = 800
    for i in range(2):
        for mt in range(1,6+1):
            pp = p if mt%2==0 else 1024-p
            servos.moveSpeedRW(mt,pp,450)
            sleep(0.01)
        servos.action()
        p = 1320 - p
        sleep(3.7)



def setup():
    global server, anglesData

    anglesData = []

    #starting oscSever
    try:
        server = MyServer()
    except ServerError, err:
        print str(err)
        sys.exit()

    print "Starting Server..."
    server.start()

    #inicializing servos
    initMotors()


if __name__=="__main__":
    setup()
    timeAverage = 0
    count = 0
    try :
       while 1:
        lastTime = time()
        if(anglesData):
            moveMotors()
        if(time()-lastTime > 0.001):
            print "%f" % (time()-lastTime)
        timeAverage += (time()-lastTime)
        count +=1
        if count >= 100:
           # print "%f" % (timeAverage/100)
            timeAverage = 0
            count = 0

    except KeyboardInterrupt :
        print  "\nStoping OSCServer."
        server.stop()
        sys.exit()

