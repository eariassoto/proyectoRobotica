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

class MainWindow(QWidget):
    """
    Tiny widget to display camera images from Naoqi.
    """
    def __init__(self, IP, PORT, parent=None):
        super(MainWindow, self).__init__()

        self._initUI()

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

        if self._ttsProxy != None:
            self._ttsProxy.say(s)


    def button2Clicked(self):
        sender = self.sender


    def __del__(self):
        """
        When the widget is deleted, we unregister our naoqi video module.
        """
        pass



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
