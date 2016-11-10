# -*- coding: utf-8 -*-
from naoqi import *
import time
import urllib2
import csv


# Get a proxy on ALBarcodeReader

ROBOT_IP = "192.168.0.101"
barcode = ALProxy("ALBarcodeReader", ROBOT_IP, 9559)
memory = ALProxy("ALMemory", ROBOT_IP, 9559)
broker = ALBroker("pythonBroker", "0.0.0.0", 0, ROBOT_IP, 9559)
tts = ALProxy("ALTextToSpeech", ROBOT_IP, 9559)
awareness = ALProxy('ALBasicAwareness', ROBOT_IP, 9559)
posture = ALProxy("ALRobotPosture", ROBOT_IP, 9559)
motion = ALProxy("ALMotion", ROBOT_IP, 9559)

posture.goToPosture("SitRelax", 1)
motion.setStiffnesses("Head", 1)

motion.setAngles("HeadYaw", 0, 0.25)
motion.setAngles("HeadPitch", 0, 0.25)
awareness.stopAwareness()



  
#url = 'http://163.178.104.75/text.csv'
#response = urllib2.urlopen(url)
#reader = csv.reader(response)
d = {"PreguntaA":"la Computación e Informática es la disciplina que estudia la resolución de problemas y el manejo automatizado de la información usando computadoras", 
"PreguntaB":"No, mas bien la carrera tiene que ver con el aprendizaje de como construir herramientas como las mencionadas o similares.",
"PreguntaC":"En realidad estos son nombres de carreras que se ofrecen en otras universidades o en las sedes regionales de la Universidad de Costa Rica; Aunque no representan disciplinas distintas; los programas de las carreras pueden diferir sustancialmente del que se ofrece en el bachillerato de Ciencias de la Computación e Informática.",
"PreguntaD":"Sí. La resolución de problemas demanda buenas habilidades y conocimientos en matemáticas; particularmente para el desarrollo de algoritmos nuevos o soluciones computacionales novedosas. Sin embargo; estas habilidades y conocimientos no se requieren en todas las áreas de la disciplina por igual. ",
"PreguntaE":"Actualmente se inicia con yava y se continúa con C++. Estos son los principales lenguajes de programación que se usan en las empresas desarrolladoras de software. En cursos avanzados se estudian otros lenguajes de programación como c charp; p.h.p.; paiton y yavascript; entre otros.",
"PreguntaF":"¡Estamos muy emocionados! A partir del próximo año se ofrecerán tres énfasis: Ciencias de la computación; ingeniería de software y tecnologías de la información. Pueden consultar la información en los carteles o bien pueden preguntar a mis amigos humanos más detalles." ,
"PreguntaG":"Sí. Existe una carrera de maestría profesional y una carrera de maestría académica. Además se ofrece el doctorado en computación.", 
"PreguntaH":"En la Universidad de Costa Rica existe un costo único para el crédito en cualquier carrera; este costo se reduce dependiendo del tipo de beca que le asigne a cada solicitante la oficina correspondiente. Puede preguntar a los humanos que me acompañan sobre más detalles.", 
"PreguntaI":"Como estudiante de primer ingreso el único requisito es aprobar el examen de admisión con una nota suficiente para optar por un puesto entre los 145 primeros solicitantes.",
"PreguntaJ":"Actualmente se cuenta con suficientes computadores para satisfacer las necesidades de los estudiantes. Los laboratorios permanecen abiertos de lunes a viernes de 7 a.m. a 9 p.m.; y sábados y domingos de 8 a.m. a 6 p.m. Por tanto NO es necesario que el estudiante posea una computadora propia.", 
"PreguntaK":"Es aconsejable pero no imprescindible tener conocimientos muy básicos del uso de computadores.",
"PreguntaL":"Es muy aconsejable que el estudiante pueda leer con fluidez literatura técnica específicamente de computación. La lectura fluida de textos simples o básicos en inglés es una condición favorable al ingresar a la carrera.",
"PreguntaM":"La carrera de bachillerato en Computación e Informática está planeada para cuatro años; aunque algunos estudiantes no logran terminarla en ese tiempo",
"PreguntaN":"Actualmente la mayoría de los cursos se dictan en un horario de 7 a.m. a las 5 p.m. En muy pocos casos hay cursos después de las 5. Se trata de una carrera diurna y de dedicación a tiempo completo.",
}

#d = {}
#for row in reader:
 #  k, v = row
  # d[k] = v

# Handler class
class myEventHandler(ALModule):
  def myCallback(self, key, value, msg):
	global d
	if value != []:
		mensaje = value[0][0]
		res = d[mensaje]
		print "Received \"" + str(key) + "\" event with data: " + str(mensaje)
		memory.unsubscribeToEvent("BarcodeReader/BarcodeDetected", "handlerModule")
		awareness.startAwareness()
		tts.say(res)
		memory.subscribeToEvent("BarcodeReader/BarcodeDetected", "handlerModule", "myCallback")
		#awareness.stopAwareness()
		motion.setAngles("HeadYaw", 0, 0.25)
		motion.setAngles("HeadPitch", 0, 0.25)
		

# Subscribe to the event (this will start the module)
handlerModule = myEventHandler("handlerModule")

memory.subscribeToEvent("BarcodeReader/BarcodeDetected", "handlerModule", "myCallback")

while True:
  time.sleep(1)
	
time.sleep(20) # Keep the broker alive for 20 seconds	

# Unsubscribe to event
memory.unsubscribeToEvent("BarcodeReader/BarcodeDetected", "handlerModule")