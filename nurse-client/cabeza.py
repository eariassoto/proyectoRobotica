# -*- encoding: UTF-8 -*-

import sys
import time
from naoqi import ALProxy
import almath
import random

tecla = 0

def wait():
	global tecla
	tecla = '\x1b[C'


def moveHead(motionProxy):
	#ARRIBA
	if tecla == '\x1b[A':
		motionProxy.setAngles("HeadPitch", 0.6,0.6)
	#ABAJO
	elif tecla == '\x1b[B':
		motionProxy.setAngles("HeadPitch",0.2,0.6)	
	#DERECHA	
	elif tecla == '\x1b[C':
		motionProxy.setAngles("HeadYaw", 0.6,0.6)
	#IZQUIERDA
	elif tecla == '\x1b[D':
		motionProxy.setAngles("HeadYaw", 0.6,0.6)

def main(robotIP):
	PORT = 9559

	try:
		motionProxy = ALProxy("ALMotion", robotIP, PORT)
	except Exception,e:
		print "Could not create proxy to ALMotion"
		print "Error was: ",e
		sys.exit(1)	
	time.sleep(1.0)

	motionProxy.setStiffnesses("Head", 1)

	motionProxy.setAngles("HeadYaw", 0, 0.6)
	motionProxy.setAngles("HeadPitch", 0.0, 0.6)


if __name__ == "__main__":
	robotIp = "10.1.133.239"

	if len(sys.argv) <= 1:
		print "Usage python almotion_angleinterpolation.py robotIP (optional default: 127.0.0.1)"
	else:
		robotIp = sys.argv[1]

	main(robotIp)