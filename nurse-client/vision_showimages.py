# -*- encoding: UTF-8 -*-
#
# This is a tiny example that shows how to show live images from Nao using PyQt.
# You must have python-qt4 installed on your system.
#

import sys
from PyQt4.QtCore import QThread
from PyQt4.QtGui import(
    QWidget,
    QImage,
    QApplication,
    QPainter,
    QDesktopWidget,
    QPushButton,
    QTextEdit
)
from naoqi import ALProxy
from time import sleep
import pdb

# To get the constants relative to the video.
import vision_definitions

image = QImage("2.png")

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
            alImage = self._videoProxy.getImageRemote(self._imgClient)
            image = QImage(alImage[6],           # Pixel array.
                                 alImage[0],           # Width.
                                 alImage[1],           # Height.
                                 QImage.Format_RGB888)
	    #del alImage
 
    def run(self):
        while True:
            self._updateImage()
            self._windows.update()
            sleep(0.1)


class ImageWidget(QWidget):
    """
    Tiny widget to display camera images from Naoqi.
    """
    def __init__(self, IP, PORT, CameraID, parent=None):
        super(ImageWidget, self).__init__()        
        self.resize(800, 600)
        
        self.center()

        btn1 = QPushButton("Button 1", self)
        btn1.move(330, 310)
        #btn1.clicked.connect(self.buttonClicked)

        self.edit = QTextEdit(self)
        self.edit.setPlainText("text")
        self.edit.setMinimumSize(200, 300)
        self.edit.move(330, 0)

        self.setWindowTitle('Nurse Client')
        self.show() 

        image = QImage("2.png")
        self.setWindowTitle('Nao')

        self._imgWidth = 320
        self._imgHeight = 240
        self._cameraID = CameraID

        # Proxy to ALVideoDevice.
        self._videoProxy = None

        # Our video module name.
        self._imgClient = ""

        self._registerImageClient(IP, PORT)

        self.myThread = NaoCameraUpdater(self._videoProxy, 
            self._imgClient, self)
        self.myThread.start()


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def _registerImageClient(self, IP, PORT):
        """
        Register our video module to the robot.
        """
        self._videoProxy = ALProxy("ALVideoDevice", IP, PORT)
        resolution = vision_definitions.kQVGA  # 320 * 240
        colorSpace = vision_definitions.kRGBColorSpace
        self._imgClient = self._videoProxy.subscribe("_client", resolution, colorSpace, 5)

        # Select camera.
        self._videoProxy.setParam(vision_definitions.kCameraSelectID,
                                  self._cameraID)


    def _unregisterImageClient(self):
        """
        Unregister our naoqi video module.
        """
        if self._imgClient != "":
            self._videoProxy.unsubscribe(self._imgClient)


    def paintEvent(self, event):
        """
        Draw the QImage on screen.
        """
        global image
        painter = QPainter(self)
        painter.drawImage(0, 0, image, 0, 0, 320, 240)


    def __del__(self):
        """
        When the widget is deleted, we unregister our naoqi video module.
        """
        self._unregisterImageClient()



if __name__ == '__main__':
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
    myWidget = ImageWidget(IP, PORT, CameraID)
    myWidget.show()
    sys.exit(app.exec_())

