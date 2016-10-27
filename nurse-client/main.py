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

# To get the constants relative to the video.
import vision_definitions

image = QImage("2.png")

"""
# Thread class template

class YourThreadName(QThread):

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        # your logic here

"""

class NaoCameraUpdater(QThread):

    def __init__(self, _videoProxy, _imgClient, _windows):
        QThread.__init__(self)
        self._videoProxy = _videoProxy
        self._imgClient = _imgClient
        self._windows = _windows

    def __del__(self):
        self.wait()
        
    def _updateImage(self):
        global image
        if self._imgClient != None:
            #alImage = self._videoProxy.getImageRemote(self._imgClient)
            #image = QImage(alImage[6],           # Pixel array.
            #                     alImage[0],           # Width.
            #                     alImage[1],           # Height.
            #                     QImage.Format_RGB888)
	    #del alImage
            pass
		 
    def run(self):
        global image
        while True:
            self._updateImage()
            self._windows.repaint()
            sleep(0.1)

class MainWindow(QWidget):
    """
    Tiny widget to display camera images from Naoqi.
    """
    def __init__(self, IP, PORT, CameraID, parent=None):
        super(MainWindow, self).__init__()

        self._cameraID = CameraID

        self._initUI()

        try:
            self._videoProxy = ALProxy("ALVideoDevice", IP, PORT)
        except:
            self._videoProxy = None
            logging.warning("No se pudo conectar al modulo ALVideoDevice")

        try:
            self._postureProxy = ALProxy("ALRobotPosture", IP, PORT)
        except:
            self._postureProxy = None
            logging.warning("No se pudo conectar al modulo ALRobotPosture")

        try:
            self._ttsProxy = ALProxy("ALTextToSpeech", IP, PORT)
        except:
            self._postureProxy = None
            logging.warning("No se pudo conectar al modulo ALTextToSpeech")

        self._registerClients()

        self._initRobot()

        self.myThread = NaoCameraUpdater(self._videoProxy, 
            self._imgClient, self)
        self.myThread.start()

    def _initUI(self):

        self.resize(800, 600)
        self.center()

        btn1 = QPushButton("Button 1", self)
        btn1.move(330, 310)
        btn1.clicked.connect(self.buttonClicked)

        self.edit = QTextEdit(self)
        self.edit.setPlainText("text")
        self.edit.setMinimumSize(200, 300)
        self.edit.move(330, 0)

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


    def _registerClients(self):
        """
        Register our video module to the robot.
        """
        if self._videoProxy != None:
            resolution = vision_definitions.kQVGA  # 320 * 240
            colorSpace = vision_definitions.kRGBColorSpace
            self._imgClient = self._videoProxy.subscribe("_client", resolution, colorSpace, 5)
            # Select camera.
            self._videoProxy.setParam(vision_definitions.kCameraSelectID,
                                      self._cameraID)
        else:
            self._imgClient = None
            logging.warning("No se pudo registrar el cliente de la camara")


    def _unregisterClients(self):
        """
        Unregister our naoqi video module.
        """
        if self._imgClient != None:
            self._videoProxy.unsubscribe(self._imgClient)


    def paintEvent(self, event):
        """
        Draw the QImage on screen.
        """
        #global image
        #painter = QPainter(self)
        #painter.drawImage(0, 0, image, 0, 0, 320, 240)
        pass

    def buttonClicked(self):
        sender = self.sender
        s = str(self.edit.toPlainText())

        if self._ttsProxy != None:
            self._ttsProxy.say(s)


    def __del__(self):
        """
        When the widget is deleted, we unregister our naoqi video module.
        """
        self._unregisterClients()



if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    IP = "10.1.133.239"  # Replace here with your NaoQi's IP address.
    PORT = 9559
    CameraID = 0

    # Read IP address from first argument if any.
    if len(sys.argv) > 1:
        IP = sys.argv[1]

    # Read CameraID from second argument if any.
    if len(sys.argv) > 2:
        CameraID = int(sys.argv[2])


    app = QApplication(sys.argv)
    myWidget = MainWindow(IP, PORT, CameraID)
    sys.exit(app.exec_())
