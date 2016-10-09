
import sys
from PyQt4 import QtGui


class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):               
        
        self.resize(800, 600)
        self.center()

        btn1 = QtGui.QPushButton("Button 1", self)
        btn1.move(300, 0)
        btn1.clicked.connect(self.buttonClicked)

        self.edit = QtGui.QTextEdit(self)
        self.edit.setPlainText("text")
        self.edit.setMinimumSize(200, 300)
        self.edit.move(0, 0)
 
        self.setWindowTitle('Nurse Client')    
        self.show()
        
    def center(self):
        
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def buttonClicked(self):

        sender = self.sender
        print(self.edit.toPlainText()) 
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()     
