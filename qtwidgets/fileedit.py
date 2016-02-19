# -*- coding: utf-8 -*-
import os
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QApplication, QWidget, QHBoxLayout, QLineEdit, QToolButton, QIcon, QFileDialog


class FilenameEdit(QWidget):

    filename_changed = pyqtSignal()

    EDIT_EXISTING_FILENAME = object()
    EDIT_NEW_FILENAME = object()
    EDIT_EXISTING_DIRECTORY = object()

    DEFAULT_CAPTION = {
        EDIT_EXISTING_FILENAME: "Open File",
        EDIT_NEW_FILENAME: "Create File",
        EDIT_EXISTING_DIRECTORY: "Open Directory",
    }
    DEFAULT_PATTERN = {
        EDIT_EXISTING_FILENAME: "All files (*)",
        EDIT_NEW_FILENAME: "All files (*)",
        EDIT_EXISTING_DIRECTORY: ""
    }

    def __init__(self, parent=None, filename=None, caption=None, pattern=None, kind=None, **kwargs):
        QWidget.__init__(self, parent, **kwargs)
        if kind is None:
            kind = self.EDIT_EXISTING_FILENAME
        if caption is None:
            caption = self.DEFAULT_CAPTION[kind]
        self._caption = caption
        if pattern is None:
            pattern = self.DEFAULT_PATTERN[kind]
        self._kind = kind
        self._pattern = pattern
        self._layout = QHBoxLayout(self)
        self._lineedit = QLineEdit(self)
        self._button = QToolButton(self)
        if kind is self.EDIT_EXISTING_DIRECTORY:
            icon = QIcon.fromTheme("document-open-folder")
        else:
            icon = QIcon.fromTheme("document-open")
        self._button.setIcon(icon)
        self._button.clicked.connect(self._on_button_clicked)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self._lineedit)
        self.layout().addWidget(self._button)
        self.set_filename(filename or "")

    def _on_button_clicked(self):
        filename = unicode(self._lineedit.text())
        if self._kind is self.EDIT_EXISTING_DIRECTORY:
            path = filename
            if not path:
                path = os.getcwd()
            filename = QFileDialog.getExistingDirectory(
                self, self._caption, path)
        else:
            if not filename:
                path = os.getcwd()
            else:
                path = os.path.dirname(filename)
            if self._kind is self.EDIT_NEW_FILENAME:
                filename = QFileDialog.getSaveFileName(
                    self, self._caption, path, self._pattern)
            else:
                assert self._kind is self.EDIT_EXISTING_FILENAME
                filename = QFileDialog.getOpenFileName(
                    self, self._caption, path, self._pattern)

        if filename:
            self.set_filename(filename)

    def filename(self):
        return unicode(self._lineedit.text()) or None

    def set_filename(self, value):
        self._lineedit.setText(value)
        self.filename_changed.emit()


class FileOpenEdit(FilenameEdit):

    def __init__(self, parent=None, filename=None, caption=None, pattern=None, **kwargs):
        FilenameEdit.__init__(
            self, parent, filename, caption, pattern, self.EDIT_EXISTING_FILENAME, **kwargs)


class DirectoryEdit(FilenameEdit):

    def __init__(self, parent=None, filename=None, caption=None, **kwargs):
        FilenameEdit.__init__(
            self, parent, filename, caption, None, self.EDIT_EXISTING_DIRECTORY, **kwargs)

    def set_directory(self, path):
        self.set_filename(path)

    def directory(self):
        return self.filename()


if __name__ == "__main__":
    app = QApplication([])
    win = DirectoryEdit(None, "/etc/")
    win.resize(400, 200)
    win.show()
    app.exec_()
    print win.filename()
