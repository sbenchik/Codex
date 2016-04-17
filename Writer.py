import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

app = QApplication(sys.argv)
from writerqsci import mainWindow
m = mainWindow()
m.show()
app.exec_()
