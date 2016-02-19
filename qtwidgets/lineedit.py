# -*- coding: utf-8 -*-
"""
From http://labs.trolltech.com/blogs/2007/06/06/lineedit-with-a-clear-button/
and arora-browser/src/utils/lineedit.{cpp,h}
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class LineEditButton(QToolButton):

    def __init__(self, parent, iconname):
        QToolButton.__init__(self, parent)
        pixmap = QPixmap(iconname)
        self.setIcon(QIcon(pixmap))
        self.setIconSize(QSize(16, 16))  # pixmap.size()
        self.setCursor(Qt.ArrowCursor)
        self.setPopupMode(QToolButton.InstantPopup)
        self.setStyleSheet(
            "QToolButton { border: none; padding: 0px; }")


class LineEditSide:
    Left = 1
    Right = 2


class LineEdit(QLineEdit):

    def __init__(self, parent=None, inactive=""):
        QLineEdit.__init__(self, parent)

        import qtwidgets.lineedit_icons

        self.left = QWidget(self)
        self.left_layout = QHBoxLayout(self.left)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.right = QWidget(self)
        self.right_layout = QHBoxLayout(self.right)
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.inactive_text = inactive

    def add_widget(self, widget, side):
        if side == LineEditSide.Left:
            layout = self.left_layout
            layout.addWidget(widget)
        else:
            layout = self.right_layout
            layout.insertWidget(1, widget)
        self.update_geometry()

    def remove_widget(self, widget):
        self.left_layout.removeWidget(widget)
        self.right_layout.removeWidget(widget)

    def update_geometry(self):
        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        self.setStyleSheet(
            "QLineEdit { padding-left: %spx; padding-right: %spx; } " % (
                self.left.sizeHint().width() + frameWidth + 1,
                self.right.sizeHint().width() + frameWidth + 1)
        )
        msz = self.minimumSizeHint()
        self.setMinimumSize(
            max(msz.width(),
                self.right.sizeHint(
                ).height() + frameWidth * 2 + 2),
            max(msz.height(),
                self.right.sizeHint().height() + frameWidth * 2 + 2))

    def resizeEvent(self, event):
        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        rect = self.rect()
        left_hint = self.left.sizeHint()
        right_hint = self.right.sizeHint()
        self.left.move(frameWidth + 1,
                      (rect.bottom() + 1 - left_hint.height()) / 2)
        self.right.move(rect.right() - frameWidth - right_hint.width(),
                        (rect.bottom() + 1 - right_hint.height()) / 2)

    def add_clear_button(self):
        self.clear_button = LineEditButton(self, ":edit-clear.png")
        self.add_widget(self.clear_button, LineEditSide.Right)
        # self.clear_button.hide()
        self.connect(self.clear_button, SIGNAL("clicked()"), self.clear)
        self.connect(self, SIGNAL("textChanged(const QString&)"),
                     self.update_clear_button)

    def update_clear_button(self, text):
        self.clear_button.setVisible(not text.isEmpty())

    def textMargin(self, side):
        if side == LineEditSide.Left:
            spacing = self.left_layout.spacing()
            w = self.left.sizeHint().width()
        else:
            spacing = self.right_layout.spacing()
            w = self.right.sizeHint().width()
        return w + spacing * 2

    def paintEvent(self, event):
        QLineEdit.paintEvent(self, event)
        if self.text().isEmpty() and \
           self.inactive_text and \
           not self.hasFocus():

            panel = QStyleOptionFrameV2()
            self.initStyleOption(panel)
            textRect = self.style().subElementRect(
                QStyle.SE_LineEditContents, panel, self)
            horizontalMargin = 2
            textRect.adjust(horizontalMargin, 0, 0, 0)

            # if QT_VERSION >= 0x040500
            left = self.textMargin(LineEditSide.Left)
            right = self.textMargin(LineEditSide.Right)
            textRect.adjust(left, 0, -right, 0)
            # endif

            painter = QPainter(self)
            painter.setPen(
                self.palette().brush(
                    QPalette.Disabled, QPalette.Text).color())
            painter.drawText(
                textRect, Qt.AlignLeft | Qt.AlignVCenter, self.inactive_text)
