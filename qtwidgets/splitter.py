# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *


# Ported from minisplitter.{h,cpp} included in QtCreator
class StyleHelper(object):

    def baseColor(self):
        return QColor(0x666666)

    def borderColor(self):
        result = self.baseColor()
        result.setHsv(result.hue(),
                      result.saturation(),
                      result.value() / 2)
        return result


StyleHelper.instance = StyleHelper()


class SplitterHandle(QSplitterHandle):

    def __init__(self, orientation, parent):
        QSplitterHandle.__init__(self, orientation, parent)
        self.setMask(QRegion(self.contentsRect()))
        self.setAttribute(Qt.WA_MouseNoMask, True)

    def resizeEvent(self, event):
        if self.orientation() == Qt.Horizontal:
            self.setContentsMargins(2, 0, 2, 0)
        else:
            self.setContentsMargins(0, 2, 0, 2)
        self.setMask(QRegion(self.contentsRect()))
        return QSplitterHandle.resizeEvent(self, event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(event.rect(), StyleHelper.instance.borderColor())


class Splitter(QSplitter):

    def __init__(self, parent):
        QSplitter.__init__(self, parent)
        self.setHandleWidth(1)
        self.setChildrenCollapsible(False)

    def createHandle(self):
        return SplitterHandle(self.orientation(), self)
