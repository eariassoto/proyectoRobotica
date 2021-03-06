# -*- encoding: UTF-8 -*-
#
# This is a tiny example that shows how to show live images from Nao using PyQt.
# You must have python-qt4 installed on your system.
#
from time import sleep
import logging, sys
from PyQt4.QtGui import(
	QWidget,
	QImage,
	QApplication,
	QPainter,
	QDesktopWidget,
	QPushButton,
	QTextEdit
)
from PyQt4.QtCore import QThread
from naoqi import ALProxy,ALModule,ALBroker
import pdb
from urllib2 import urlopen
from threading import Thread, BoundedSemaphore
from json import loads
from datetime import datetime
from gtts import gTTS
from vlc import MediaPlayer

# To get the constants relative to the video.
import vision_definitions


# Este es un patrón de diseño que es parecido al Singleton.
# En este patrón se hacen múltiples instancias de la clase pero
# todas comparten el mismo estado (el self.loquesea es igual en 
# todas). Util para compartir variables entre hilos 
class Borg:
	_shared_state = {}
	def __init__(self):
		self.__dict__ = self._shared_state

# esta clase tiene un array de alertas, las alertas son un par de(int, string)
# el int es el codigo (asuma que es único) y el string es el mensaje. Si se 
# intenta meter un mensaje con un id que ya está incluido se ignora.
class Alert_Manager(Borg):
	def __init__(self, txtArea=None):
		Borg.__init__(self)
		if txtArea != None:
			self.txtArea = txtArea
				
		
	# todo: revisar si el id ya está incluido no se mete en el array y se devuelve -1
	# todo2: cuando el txtArea sea valido actualizarlo
	def insert_alert(self, id, msg):
		# el try catch es porque self.alerts no existe en el 
		# estado inicial
		s_timespamp = datetime.now().strftime('%d-%m-%Y %I:%M %p')
		try:
			self.alerts.append((id, s_timespamp, msg))
		except:
			self.alerts = [(id, s_timespamp, msg)]

		s = ""
		for a in self.alerts:
			# dejo el s[0] para debugging
			s += str(a[1]) + " - " + str(a[2]) + "\n"
		self.txtArea.setPlainText( s )
		tts = gTTS(text=msg, lang='es')
		tts.save("msg.mp3")
		p = MediaPlayer("msg.mp3")
		p.play()
			
		return id
	
	# todo: implementar esto y que actualize el estado de las alertass
	def remove_alert(self, id):
		pass
		
	def is_empty(self):
		return len(self.alerts) == 0
		
	def get_alerts(self):
		return self.alerts

class Revisa_Signos(Thread):
	def __init__ (self, sema, delay, fiebre, direccion_api):
		Thread.__init__(self)
		self.delay = delay
		self.fiebre = fiebre
		self.direccion_api = direccion_api
		self.sema = sema
		
		self.alert = Alert_Manager()

	def run(self):
		error = False
		while not self.sema.acquire(False) and not error:
			try:
				request = urlopen(self.direccion_api).read()
				request = loads(request)
				temp = request['temperatura']
				if temp >= self.fiebre:
					self.alert.insert_alert("El paciente tiene fiebre!")
					# todo, mandar la alerta a self.alert
			except:
				print("error al abrir la conexion, saliendo")
				error = True
			sleep(self.delay)
		if not error: # salio por curso normal
			self.sema.release()


# Handler class
class myEventHandler(ALModule):
  def myCallback(self, key, value, msg):
    print "Received \"" + str(key) + "\" event with data: " + str(value)
			
class MainWindow(QWidget):
	"""
	Tiny widget to display camera images from Naoqi.
	"""
	def __init__(self, IP, PORT, parent=None):
		super(MainWindow, self).__init__()
		self._initUI()

		# ocupo este semaforo para que cuando la ventana muera
		# este hilo muera tambien
		self.sema = BoundedSemaphore()
		self.sema.acquire()
		
		self.alert = Alert_Manager(self.alertTextArea)
		
		self.thread_revisa = Revisa_Signos(self.sema, 2, 28.00, 'http://127.0.0.1:3000')
		self.thread_revisa.start()
		
		self.cabezaX = 0
		self.cabezaY = 0
		
		#try:
		self._ttsProxy = ALProxy("ALTextToSpeech", IP, PORT)
		self._postureProxy = ALProxy("ALRobotPosture", IP, PORT)
		self._barcodeProxy = ALProxy("ALBarcodeReader", IP, PORT)
		self._awarenessProxy = ALProxy('ALBasicAwareness', IP, PORT)
		self._motionProxy = ALProxy("ALMotion", IP, PORT)

		self._initRobot()
		
		"""except:
			self._postureProxy = None
			self._ttsProxy = None
			self._barcodeProxy = None
			self._memoryProxy = None
			self._awarenessProxy = None
			self._memoryProxy = None
			self._memoryProxy = None
			logging.warning("No se pudo conectar al robot")"""


	def _initUI(self):

		self.resize(800, 600)
		self.center()

		btn1 = QPushButton("Button 1", self)
		btn1.move(330, 310)
		btn1.clicked.connect(self.button1Clicked)

		btnDer = QPushButton("Derecha", self)
		btnDer.move(0, 0)
		btnDer.clicked.connect(self.buttonDerClicked)

		btnIzq = QPushButton("Izquierda", self)
		btnIzq.move(100, 0)
		btnIzq.clicked.connect(self.buttonIzqClicked)

		btnArr = QPushButton("Arriba", self)
		btnArr.move(0, 100)
		btnArr.clicked.connect(self.buttonArrClicked)

		btnAba = QPushButton("Abajo", self)
		btnAba.move(100, 100)
		btnAba.clicked.connect(self.buttonAbaClicked)

		self.edit = QTextEdit(self)
		self.edit.setPlainText("Hola Mundo")
		self.edit.setMinimumSize(200, 300)
		self.edit.move(330, 0)
		
		self.alertTextArea = QTextEdit(self)
		self.alertTextArea.setReadOnly = True
		self.alertTextArea.setPlainText("TODO")
		self.alertTextArea.setMinimumSize(200, 300)
		self.alertTextArea.move(550, 0)
		
		self.setWindowTitle('Nurse Client')	
		self.show()

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())


	def _initRobot(self):
		if self._postureProxy != None:
			pos = "Sit"
			logging.info("Postura seleccionada: " + pos)
			self._postureProxy.goToPosture(pos, 1.0)
		if self._awarenessProxy != None:
			self._awarenessProxy.stopAwareness()
			# ponerla tiesa
		if self._motionProxy != None:
			self._motionProxy.setStiffnesses("Head", 1)
			self._motionProxy.setAngles("HeadYaw", 0, 0.5)
			self._motionProxy.setAngles("HeadPitch", 0.0, 0.5)


	def button1Clicked(self):
		sender = self.sender
		s = str(self.edit.toPlainText())
		
		try:
			self._ttsProxy.say(s)
		except:
			pass
			
		self.alert.insert_alert(1, s)


	def buttonDerClicked(self):
		if self.cabezaX != -1:
			self.cabezaX -= 0.1
		self._motionProxy.setAngles("HeadYaw", self.cabezaX, 0.3)

	def buttonIzqClicked(self):
		if self.cabezaX != 1:
			self.cabezaX += 0.1
		self._motionProxy.setAngles("HeadYaw", self.cabezaX, 0.3)

	def buttonArrClicked(self):
		if self.cabezaY != -0.5:
			self.cabezaY -= 0.1
		self._motionProxy.setAngles("HeadPitch", self.cabezaY, 0.3)

	def buttonAbaClicked(self):
		if self.cabezaY != 0.5:
			self.cabezaY += 0.1
		self._motionProxy.setAngles("HeadPitch", self.cabezaY, 0.3)


	def __del__(self):
		pass
		
	def closeEvent(self, event):
		self.sema.release()


if __name__ == '__main__':
	IP = "10.1.133.239"  # Replace here with your NaoQi's IP address.
	PORT = 9559

	broker = ALBroker("pythonBroker","0.0.0.0", 0, IP, PORT)
	handlerModule = myEventHandler("handlerModule")
        memory = ALProxy("ALMemory", IP, PORT)

	memory.subscribeToEvent("BarcodeReader/BarcodeDetected", "handlerModule", "myCallback")
	logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

	# Read IP address from first argument if any.
	if len(sys.argv) > 1:
		IP = sys.argv[1]

	app = QApplication(sys.argv)
	myWidget = MainWindow(IP, PORT)
	#memory.unsubscribeToEvent("BarcodeReader/BarcodeDetected", "handlerModule")
	sys.exit(app.exec_())
