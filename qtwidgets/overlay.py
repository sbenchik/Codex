# -*- coding: utf-8 -*-
# From http://wiki.qtcentre.org/index.php?title=Widget_Overlay
from PyQt4.QtCore import Qt
from PyQt4.QtGui import *


class Overlay(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        palette = QPalette(self.palette())
        palette.setColor(palette.Background, Qt.transparent)
        self.setPalette(palette)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
