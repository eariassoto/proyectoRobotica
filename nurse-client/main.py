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
from naoqi import ALProxy
import pdb
from urllib2 import urlopen
from threading import Thread, BoundedSemaphore
from json import loads

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
		try:
			self.alerts.append((id, msg))
		except:
			self.alerts = [(id, msg)]
		# todo: si se agrega el elemento actualizar el txtarea
		# le caigo encima al texto por probar
		# self.textArea tiene los metodos append, clear y este otro
		# También dejo la doc http://pyqt.sourceforge.net/Docs/PyQt4/qtextedit.html
		self.txtArea.setPlainText( msg )
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
					print("El paciente tiene fiebre!")
					# todo, mandar la alerta a self.alert
			except:
				print("error al abrir la conexion, saliendo")
				error = True
			sleep(self.delay)
		if not error: # salio por curso normal
			self.sema.release()


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
		
		try:
			self._ttsProxy = ALProxy("ALTextToSpeech", IP, PORT)
		except:
			self._postureProxy = None
			logging.warning("No se pudo conectar al modulo ALTextToSpeech")

		#self._initRobot()


	def _initUI(self):

		self.resize(800, 600)
		self.center()

		btn1 = QPushButton("Button 1", self)
		btn1.move(330, 310)
		btn1.clicked.connect(self.button1Clicked)

		btn2 = QPushButton("Derecha", self)
		btn2.move(0, 0)
		btn2.clicked.connect(self.button2Clicked)

		self.edit = QTextEdit(self)
		self.edit.setPlainText("text")
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


	def button1Clicked(self):
		sender = self.sender
		s = str(self.edit.toPlainText())
		
		try:
			self._ttsProxy.say(s)
		except:
			pass
			
		self.alert.insert_alert(1, s)


	def button2Clicked(self):
		sender = self.sender


	def __del__(self):
		pass
		
	def closeEvent(self, event):
		self.sema.release()



if __name__ == '__main__':
	logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

	IP = "10.1.133.239"  # Replace here with your NaoQi's IP address.
	PORT = 9559

	# Read IP address from first argument if any.
	if len(sys.argv) > 1:
		IP = sys.argv[1]

	app = QApplication(sys.argv)
	myWidget = MainWindow(IP, PORT)
	sys.exit(app.exec_())
