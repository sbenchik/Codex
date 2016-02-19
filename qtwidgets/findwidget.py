# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *


try:
    i18n
except NameError:
    # no such builtin
    i18n = unicode


class CheckAction(QAction):

    def __init__(self, parent, text, checked=False):
        QAction.__init__(self, text, parent)
        self.setCheckable(True)
        self.setChecked(checked)


class FindButton(QToolButton):

    def __init__(self, parent, label, icon, callback):
        QToolButton.__init__(self, parent)
        self.setAutoRaise(True)
        if icon:
            self.setIcon(QIcon(QPixmap(icon)))
            self.setIconSize(QSize(16, 16))
        if label:
            self.setText(label)
            self.setToolTip(label)
            self.set_label_visible(True)
        self.connect(self, SIGNAL("clicked()"), callback)

    def set_label_visible(self, flag=True):
        if flag:
            self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        else:
            self.setToolButtonStyle(Qt.ToolButtonIconOnly)


class FindDirection(object):
    Forward = 1
    Backward = 2


class FindWidget(QWidget):

    def __init__(self, parent, textedit=None,
                 direction=FindDirection.Forward, use_menu=False):
        QWidget.__init__(self, parent)
        self.setContentsMargins(1, 1, 1, 1)
        # Import on first use
        import qtwidgets.findwidget_icons
        from qtwidgets.flowlayout import FlowLayout

        self.textedit = textedit or parent
        self.direction = direction

        self.flow = FlowLayout(self)
        self.setLayout(self.flow)

        self.close_button = FindButton(
            self, None, ":window-close.png", self.hide)
        self.close_button.setToolTip(i18n("Close"))
        self.layout().addWidget(self.close_button)

        self.spacer = QWidget(self)
        self.spacer.setFixedSize(QSize(8, 8))
        self.layout().addWidget(self.spacer)

        self.find_label = QLabel(i18n("&Find:"), self)
        self.layout().addWidget(self.find_label)

        if use_menu:
            from lineedit import LineEdit, LineEditButton, LineEditSide
            self.text = LineEdit(self)
            self.options = LineEditButton(self.text, ":find-menu.png")
            self.text.add_widget(self.options, LineEditSide.Right)

        else:
            self.text = QLineEdit(self)

        self.text_pal = QPalette(self.text.palette())
        self.connect(self.text,
                     SIGNAL("textChanged(const QString&)"), self.search_inc)
        self.connect(self.text, SIGNAL("returnPressed()"), self.search_next)
        self.find_label.setBuddy(self.text)
        self.layout().addWidget(self.text)

        self.backward_button = FindButton(
            self, i18n("&Backward"), ":go-previous.png", self.search_backward)
        self.layout().addWidget(self.backward_button)

        self.forward_button = FindButton(
            self, i18n("For&ward"), ":go-next.png", self.search_forward)
        self.layout().addWidget(self.forward_button)

        if use_menu:
            self.menu = QMenu("Options")
            self.inc = CheckAction(self.menu, i18n("&Incremental"), True)
            self.menu.addAction(self.inc)
            self.cs = CheckAction(self.menu, i18n("&Case sensitive"))
            self.menu.addAction(self.cs)
            self.words = CheckAction(self.menu, i18n("Whole &world only"))
            self.menu.addAction(self.words)
            self.options.setMenu(self.menu)

        else:
            self.inc = QCheckBox(i18n("&Incremental"), self)
            self.inc.setChecked(True)
            self.layout().addWidget(self.inc)

            self.cs = QCheckBox(i18n("&Case sensitive"), self)
            self.layout().addWidget(self.cs)

            self.words = QCheckBox(i18n("Whole &words"), self)
            self.layout().addWidget(self.words)

        self.buttons = [self.close_button, self.forward_button,
                        self.backward_button]

    def search_inc(self, text):

        if not self.inc.isChecked():
            return

        cursor = self.textedit.textCursor()
        if cursor.hasSelection():
            cursor.setPosition(
                cursor.selectionStart(), QTextCursor.MoveAnchor)
            self.textedit.setTextCursor(cursor)
        self.search_next()

    def search_forward(self):
        self.direction = FindDirection.Forward
        return self.search_next()

    def search_backward(self):
        self.direction = FindDirection.Backward
        return self.search_next()

    def search_next(self, *args):
        # XXX: look into qt/tools/assistant/tabbedbrowser.cpp:find
        options = QTextDocument.FindFlags()
        if self.cs.isChecked():
            options |= QTextDocument.FindCaseSensitively
        if self.words.isChecked():
            options |= QTextDocument.FindWholeWords
        if self.direction == FindDirection.Backward:
            options |= QTextDocument.FindBackward
        text = unicode(self.text.text())
        result = text and self.textedit.find(text, options)
        if not result:
            self.text.palette().setColor(
                self.text.backgroundRole(), QColor("red"))
            self.text.palette().setColor(
                self.text.foregroundRole(), QColor("white"))
        else:
            # restore default colors
            self.text.setPalette(self.text_pal)
        self.update()
        return result

    def resizeEvent(self, event):
        width = self.width()
        delta = event.size().width() - event.oldSize().width()
        if delta != 0:
            for button in reversed(self.buttons):
                flag = self.layout().calc_full_width() < width
                button.set_label_visible(flag)
        return QWidget.resizeEvent(self, event)


class ReplaceWidget(FindWidget):

    def __init__(self, parent, textedit=None,
                 direction=FindDirection.Forward, use_menu=True):
        FindWidget.__init__(self, parent, textedit, direction, use_menu)

        self.spacer2 = QWidget(self)
        self.spacer2.setFixedSize(QSize(24, 8))
        self.layout().addWidget(self.spacer2)

        self.replace_label = QLabel(i18n("&Replace with:"), self)
        self.layout().addWidget(self.replace_label)
        self.new_text = QLineEdit(self)
        self.connect(self.new_text, SIGNAL(
            "returnPressed()"), self.replace_next)
        self.layout().addWidget(self.new_text)
        self.replace_label.setBuddy(self.new_text)

        self.replace_backward_button = FindButton(
            self, i18n("For&ward"), ":go-previous.png", self.replace_backward)
        self.layout().addWidget(self.replace_backward_button)

        self.replace_forward_button = FindButton(
            self, i18n("For&ward"), ":go-next.png", self.replace_forward)
        self.layout().addWidget(self.replace_forward_button)

        self.replace_all_button = FindButton(
            self, i18n("Replace &All"), None, self.replace_all)
        self.layout().addWidget(self.replace_all_button)

        self.buttons.extend([
            self.replace_backward_button, self.replace_forward_button,
            self.replace_all_button])

    def replace_backward(self):
        self.direction = FindDirection.Backward
        self.replace_next()

    def replace_forward(self):
        self.direction = FindDirection.Forward
        self.replace_next()

    def replace_all(self):
        # XXX start at top?
        while True:
            if not self.replace_next():
                break

    def replace_next(self):
        cursor = self.textedit.textCursor()
        if cursor.hasSelection():
            cursor.setPosition(
                cursor.selectionStart(), QTextCursor.MoveAnchor)
            self.textedit.setTextCursor(cursor)

        result = self.search_next()
        if result:
            cursor = self.textedit.textCursor()
            cursor.removeSelectedText()
            start_pos = cursor.position()
            cursor.insertText(self.new_text.text())
            end_pos = cursor.position()
            cursor.setPosition(start_pos)
            cursor.setPosition(end_pos, QTextCursor.KeepAnchor)
            self.textedit.setTextCursor(cursor)
        return result
