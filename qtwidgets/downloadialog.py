# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *


class DownloadDialog(QProgressDialog):

    def __init__(self, parent=None):
        QProgressDialog.__init__(self,
                                 "Download",
                                 "Cancel",
                                 0,
                                 100,
                                 parent)
        self.setWindowModality(Qt.WindowModal)
        self.http = QHttp()
        self.connect(self.http,
                     SIGNAL("dataReadProgress(int,int)"),
                     self.onDataRead)
        self.connect(self.http,
                     SIGNAL("done(bool)"),
                     self.onDone)
        self.connect(self, SIGNAL("canceled()"), self.http.abort)

    def onDataRead(self, done, total):
        if total == 0:
            self.setValue(50)
        else:
            self.setValue(done / total)

    def onDone(self, error):
        if error:
            self.error = self.http.errorString()
        self.setValue(100)
        # self.close()

    def download(self, url, label=None):
        self.error = None
        url = QUrl(url)
        self.http.setHost(url.host(), url.port(80))
        username = url.userName()
        if not username.isEmpty():
            self.http.setUser(username, url.password())
        self.setLabelText(label or url.path())
        self.show()
        qApp.processEvents()
        self.http.get(url.path())

    @classmethod
    def get(cls, url, label=None):
        dlg = cls()
        dlg.download(url, label)
        dlg.exec_()
        if dlg.wasCanceled():
            return
        return dlg.http.readAll()


def download(url, label=None):
    return DownloadDialog.get(url, label)
