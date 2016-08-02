import sys, config
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Terminal(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        #self.resize(200, 40)
        self.process = QProcess(self)
        self.terminal = QWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.terminal)
        # Has to be cast to int first because winID() returns a void pointer
        wID = int(self.terminal.winId())
        self.process.start('xterm', ['-into', str(wID), '-geometry', '800x40'])
