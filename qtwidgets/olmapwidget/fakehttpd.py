# -*- coding: utf-8 -*-
import mimetypes
import os

from PyQt4.QtCore import QByteArray, QTimer, SIGNAL, QVariant, QIODevice
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest


static_folder = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "static")


mimetypes.init()


# From http://diotavelli.net/PyQtWiki/Using%20a%20Custom%20Protocol%20with%20QtWebKit
# and http://doc.qt.nokia.com/qq/32/qq32-webkit-protocols.html
class NetworkReply(QNetworkReply):

    def __init__(self, parent, request, operation, content, mime_type=None):
        QNetworkReply.__init__(self, parent)
        if isinstance(content, unicode):
            content = content.encode("utf-8")
        self.open(self.ReadOnly | self.Unbuffered)
        self.data = QByteArray(content)
        self.setRequest(request)
        self.setOpenMode(QIODevice.ReadOnly)
        self.setOperation(operation)

        if mime_type is None:
            mime_type, encoding = mimetypes.guess_type(
                unicode(request.url().path()), strict=False)
            mime_type = mime_type or "text/html"
        content_type = "%s; charset=utf-8" % mime_type
        self.setHeader(
            QNetworkRequest.ContentTypeHeader, QVariant(content_type))
        self.setHeader(QNetworkRequest.ContentLengthHeader,
                       QVariant(QByteArray.number(self.data.length())))
        # if operation is QNetworkAccessManager.PostOperation:
        #    self.setHeader("CC")
        QTimer.singleShot(0, self, SIGNAL("metaDataChanged()"))
        QTimer.singleShot(0, self, SIGNAL("readyRead()"))
        print "new reply"

    def abort(self):
        pass

    def bytesAvailable(self):
        if self.data.length() == 0:
            QTimer.singleShot(0, self, SIGNAL("finished()"))
        count = self.data.length() + QNetworkReply.bytesAvailable(self)
        return count

    def isSequential(self):
        return True

    def readData(self, maxSize):
        count = min(maxSize, self.data.length())
        data = str(self.data[:count])
        self.data.remove(0, count)
        if self.data.length() == 0:
            QTimer.singleShot(0, self, SIGNAL("finished()"))
        return data


class NetworkAccessManager(QNetworkAccessManager):

    def __init__(self, old_manager):
        QNetworkAccessManager.__init__(self)
        self.old_manager = old_manager
        self.setCache(old_manager.cache())
        self.setCookieJar(old_manager.cookieJar())
        self.setProxy(old_manager.proxy())
        self.setProxyFactory(old_manager.proxyFactory())
        print "new manager"

    def createRequest(self, operation, request, data):
        url = request.url()
        print "requesting", unicode(url)
        if url.scheme() != "http" or (url.scheme() == "http" and url.host() != "localhost.app"):
            return QNetworkAccessManager.createRequest(self, operation, request, data)
        if operation == self.GetOperation:
            #qs = unicode(url.encodedQuery())
            path = unicode(url.path())
            if path.startswith("/static"):
                filename = os.path.join(static_folder, path[8:])
                content = open(filename).read()
            else:
                raise RuntimeError("Unexpected request: %r" % path)
            reply = NetworkReply(self, request, operation, content)
            return reply
        else:
            print "Other request", operation, request, data
            for entry in request.rawHeaderList():
                print entry
            raise RuntimeError("Unexpected request %r" % request.url())
            # return QNetworkAccessManager.createRequest(self, operation,
            # request, data)


def install_fake_httpd(webview):
    # QWebSecurityOrigin.addLocalScheme("app")
    #QWebSettings.globalSettings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
    old_manager = webview.page().networkAccessManager()
    new_manager = NetworkAccessManager(old_manager)
    webview.page().setNetworkAccessManager(new_manager)
