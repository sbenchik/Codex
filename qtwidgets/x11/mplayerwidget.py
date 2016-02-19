# -*- coding: utf-8 -*-
# See http://www.mplayerhq.hu/DOCS/tech/slave.txt
# and mplayer -input cmdlist
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class MPlayerWidget(QWidget):

    cmd = "mplayer -slave -quiet -noconsolecontrols -nomouseinput -vo %(vo)s -ao %(ao)s -wid %(wid)s %(filename)r"

    cfg = dict(
        ao="alsa",
        vo="xv"
    )

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.process = None

        self.view = QLabel(self)
        self.view.setPaletteBackgroundColor(QColor(0, 0, 0))
        self.view.setPaletteForegroundColor(QColor(255, 255, 255))

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.view)

    def timerEvent(self, event):
        self.killTimers()
        if self.process:
            self.process.kill()
            self.process = None

    def start(self, filename):
        import shlex
        import atexit

        self.view.setText("<center>Loading MPlayer...</center>")
        qApp.processEvents()

        self.pause_flag = False
        self.mute_flag = False
        self.fullscreen_flag = False

        self.cfg["wid"] = self.view.winId()
        self.cfg["filename"] = filename
        args = shlex.split(self.cmd % self.cfg)

        self.process = QProcess(self)
        for a in args:
            self.process.addArgument(a)

        self.connect(self.process, SIGNAL("processExited()"), self.done)
        self.connect(self.process, SIGNAL("launchFinished()"), self.finished)
        self.connect(self.process, SIGNAL("readyReadStdout()"), self.ready)
        self.connect(self.process, SIGNAL("readyReadStderr()"), self.error)

        if not self.process.start():
            self.failed()

        atexit.register(self.exit)

    def failed(self):
        print "launch error"

    def finished(self):
        pass

    def done(self):
        code = self.process.exitStatus()
        self.process = None

    def ready(self):
        if self.started:
            self.started = False
            self.view.setText("")
            self.osd(os.path.split(self.cfg["filename"])[1])

        data = str(self.process.readStdout())
        if data.startswith("ANS_LENGTH="):
            self.time_length = int(data.split("=", 1)[1][:-1])

    def error(self):
        self.process.readStderr()

    def play(self, filename):
        self.view.setText("<center>Loading %s...</center>" % filename)
        qApp.processEvents()

        self.started = True
        self.cfg["filename"] = filename
        self.time_pos = 0
        self.time_length = 0

        if self.process:
            self("pause")
            self("loadfile %s" % filename)
        else:
            self.start(filename)

        self("pause")
        self.getTimeLength()

    def seek(self, second):
        self("seek %s 2" % second)

    def osd(self, msg):
        self("osd_show_text %s" % msg)

    def exit(self):
        if self.process:
            self("pause")
            self("quit 0")
            self.process.tryTerminate()
            self.startTimer(1000)

    def __call__(self, cmd):
        if self.process:
            try:
                self.process.writeToStdin("\n%s\n" % cmd)
            except:
                pass

    def __del__(self):
        self.exit()

    def load(self, url):
        self.cfg["filename"] = url
        self("load_file %s" % url)

    def setVolume(self, value):
        self("volume %s 1" % value)

    def getTimeLength(self):
        self("get_time_length")

    def getTimePos(self):
        self("pause")
        self("get_time_pos")
        self("pause")

    def toggle_mute(self):
        self("mute")
        self.mute_flag = not self.mute_flag

    def toggle_pause(self):
        self("pause")
        self.pause_flag = not self.pause_flag

    def pause(self):
        if not self.pause_flag:
            self.toggle_pause()

    def resume(self):
        if self.pause_flag:
            self.toggle_pause()

    def fullscreen(self):
        if not self.fullscreen_flag:
            self("vo_fullscreen")
            self.fullscreen_flag = True

    def windowed(self):
        if self.fullscreen_flag:
            self("vo_fullscreen")
            self.fullscreen_flag = False
