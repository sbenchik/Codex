# -*- coding: utf-8 -*-

from PyQt4.QtCore import Qt, SIGNAL, QTimer
from PyQt4.QtGui import QWidget, QColor, QPainter


class Fader(QWidget):
    # From http://doc.trolltech.com/qq/qq16-fader.html

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        if parent:
            self.startColor = parent.palette().window().color()
        else:
            self.startColor = QColor("white")
        self.currentAlpha = 0
        self.duration = 333

        self.timer = QTimer(self)
        self.connect(self.timer, SIGNAL("timeout()"), self.update)

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.resize(parent.size())

    def start(self):
        self.currentAlpha = 255
        self.timer.start(33)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)

        semiTransparentColor = self.startColor
        semiTransparentColor.setAlpha(self.currentAlpha)
        painter.fillRect(self.rect(), semiTransparentColor)

        self.currentAlpha -= 255 * self.timer.interval() / self.duration
        if self.currentAlpha <= 0:
            self.timer.stop()
            self.close()


# From http://www.diotavelli.net/PyQtWiki/Fading%20Between%20Widgets
class SwitchFader(QWidget):

    def __init__(self, old_widget, new_widget):
        QWidget.__init__(self, new_widget)
        self.old_pixmap = QPixmap(new_widget.size())
        old_widget.render(self.old_pixmap)
        self.pixmap_opacity = 1.0
        self.timeline = QTimeLine()
        self.timeline.valueChanged.connect(self.animate)
        self.timeline.finished.connect(self.close)
        self.timeline.setDuration(333)
        self.timeline.start()
        self.resize(new_widget.size())
        self.show()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setOpacity(self.pixmap_opacity)
        painter.drawPixmap(0, 0, self.old_pixmap)
        painter.end()

    def animate(self, value):
        self.pixmap_opacity = 1.0 - value
        self.repaint()
