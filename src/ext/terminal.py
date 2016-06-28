# From Henning Schroeder at https://bitbucket.org/henning/pyqtwidgets/
# -*- coding: utf-8 -*-
import subprocess, atexit

from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class XTerm(QX11EmbedContainer):

    def __init__(self, parent, xterm_cmd="xterm"):
        QX11EmbedContainer.__init__(self, parent)
        self.xterm_cmd = xterm_cmd
        self.process = QProcess(self)
        self.connect(self.process,
                     SIGNAL("finished(int, QProcess::ExitStatus)"),
                     self.on_term_close)
        atexit.register(self.kill)

    def kill(self):
        self.process.kill()
        self.process.waitForFinished()

    def show_term(self):
        args = [
            "-into",
            str(self.winId()),
            "-bg",
            "#000000",  # self.palette().color(QPalette.Background).name(),
            "-fg",
            "#f0f0f0",  # self.palette().color(QPalette.Foreground).name(),
            # border
            "-b", "0",
            "-w", "0",
            # blink cursor
            "-bc",
        ]
        self.checkForTerm()
        self.process.start(self.xterm_cmd, args)

    def on_term_close(self, exit_code, exit_status):
        self.close()

    def checkForTerm(self):
        if "xterm" not in str(subprocess.call("which xterm",shell=True)):
            dialog = QtGui.QMessageBox(self)
            dialog.setIcon(QtGui.QMessageBox.Warning)
            dialog.setText("XTerm not installed")
            dialog.setInformativeText("XTerm not installed")
            dialog.setStandardButtons(QtGui.QMessageBox.Cancel)
            dialog.setDefaultButton(QtGui.QMessageBox.Cancel)
