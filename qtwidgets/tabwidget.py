# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *


# Ported from http://wiki.qtcentre.org/index.php?title=Movable_Tabs

class MovableTabBar(QTabBar):

    def __init__(self, parent=None):
        QTabBar.__init__(self, parent)
        self.setAcceptDrops(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragStartPos = event.pos()
        QTabBar.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        # if (event.pos() - self.dragStartPos).manhattanLength() < \
        #      QApplication.startDragDistance():
        #    return

        drag = QDrag(self)
        mimeData = QMimeData()
        mimeData.setData("action", "tab-reordering")
        drag.setMimeData(mimeData)
        drag.exec_()

    def dragEnterEvent(self, event):
        m = event.mimeData()
        formats = m.formats()
        if formats.contains("action") and m.data("action") == "tab-reordering":
            event.acceptProposedAction()

    def dropEvent(self, event):
        fromIndex = self.tabAt(self.dragStartPos)
        toIndex = self.tabAt(event.pos())
        if fromIndex != toIndex:
            self.emit(SIGNAL("tabMoveRequested"), fromIndex, toIndex)
        event.acceptProposedAction()


class TabWidget(QTabWidget):

    def __init__(self, parent=None):
        QTabWidget.__init__(self, parent)
        self.tb = MovableTabBar(self)
        self.connect(self.tb, SIGNAL("tabMoveRequested"), self.move_tab)
        self.setTabBar(self.tb)

    def move_tab(self, fromIndex, toIndex):
        w = self.widget(fromIndex)
        icon = self.tabIcon(fromIndex)
        text = self.tabText(fromIndex)
        self.removeTab(fromIndex)
        self.insertTab(toIndex, w, icon, text)
        self.setCurrentIndex(toIndex)

    def wheelEvent(self, event):
        rect = self.tabBar().rect()
        rect.setWidth(self.width())
        if rect.contains(event.pos()):
            self.wheel_move(event.delta())

    def wheel_move(self, delta):
        count = self.count()
        if count > 1:
            current = self.currentIndex()
            if delta < 0:
                current = (current + 1) % count
            else:
                count -= 1
                if current < 0:
                    current = count - 1
            self.setCurrentIndex(current)
