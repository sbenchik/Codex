# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class SqueezeLabel(QLabel):

    def __init__(self, parent):
        QLabel.__init__(self, parent)
        self.sqeezed_cache = None

    def paintEvent(self, event):
        text = self.text()
        if (self.sqeezed_cache != text):
            self.sqeezed_cache = text
            fm = self.fontMetrics()
            if (fm.width(self.sqeezed_cache) > self.contentsRect().width()):
                elided = fm.elidedText(text, Qt.ElideMiddle, self.width())
                self.setText(elided)
        QLabel.paintEvent(self, event)
