from naoqi import ALProxy
import time 

ROBOT_IP = "";

barcode = ALProxy("ALBarcodeReader", ROBOT_IP, 9599)
barcode.suscribe("test_barcode")

memory = ALProxy("ALMemory", ROBOT_IP, 9559)

for i in  range (20):
	data = memory.getData("BarcodeReader/BarcodeDetected")
	print data 
	time.sleep(1)
