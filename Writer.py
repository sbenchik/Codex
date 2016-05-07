import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

app = QApplication(sys.argv)
import config
config.m.show()
app.exec_()
