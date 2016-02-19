#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import pickle
import atexit
import urllib
import tempfile

from PyQt4.QtCore import QSharedMemory, SIGNAL, QIODevice, QObject
from PyQt4.QtNetwork import QLocalServer, QLocalSocket
from PyQt4.QtGui import QApplication


class IpcBase(QObject):

    timeout = 1000

    class Error(Exception):
        pass

    def __init__(self, channel=None, parent=None):
        QObject.__init__(self, parent)
        self.socket_filename = os.path.expanduser(
            "~/.ipc_%s" % self.generate_unique_id(channel))
        print self.socket_filename
        self.shared_mem = QSharedMemory()
        self.shared_mem.setKey(self.socket_filename)
        if self.shared_mem.attach():
            self.is_running = True
        else:
            self.is_running = False

    def generate_unique_id(self, channel=None):
        if channel is None:
            channel = os.path.basename(sys.argv[0])

        return "%s@%s" % (
            channel,
            os.environ.get("DISPLAY", "-1")
        )


class IpcServer(IpcBase):

    def __init__(self, channel):
        IpcBase.__init__(self, channel)
        if self.is_running:
            raise self.Error("IPC server already running")
        if not self.shared_mem.create(1):
            print >>sys.stderr, "Unable to create single instance"
            return
        self.server = QLocalServer(self)
        self.connect(self.server, SIGNAL("newConnection()"),
                     self.receive_message)
        if os.path.exists(self.socket_filename):
            os.remove(self.socket_filename)
        self.server.listen(self.socket_filename)
        atexit.register(self.cleanup)

    def cleanup(self):
        os.remove(self.socket_filename)

    def receive_message(self):
        socket = self.server.nextPendingConnection()
        if not socket.waitForReadyRead(self.timeout):
            print >>sys.stderr, socket.errorString()
            return
        byte_array = socket.readAll()
        self.handle_new_message(pickle.loads(str(byte_array)))

    def handle_new_message(self, message):
        raise NotImplementedError, self.handle_new_message


class IpcClient(IpcBase):

    def __init__(self, channel):
        IpcBase.__init__(self, channel)
        if not self.is_running:
            raise self.Error(
                "Client cannot connect to IPC server. Not running.")

    def send_message(self, message):
        if not self.is_running:
            raise self.Error(
                "Client cannot connect to IPC server. Not running.")
        socket = QLocalSocket(self)
        socket.connectToServer(self.socket_filename, QIODevice.WriteOnly)
        if not socket.waitForConnected(self.timeout):
            raise self.Error(str(socket.errorString()))
        socket.write(pickle.dumps(message))
        if not socket.waitForBytesWritten(self.timeout):
            raise self.Error(str(socket.errorString()))
        socket.disconnectFromServer()


class Application(QApplication):

    def __init__(self, argv=None, application_id=None):
        if argv is None:
            argv = sys.argv
        QApplication.__init__(self, argv)
        self.ipc_server = None
        self.ipc_client = None
        try:
            ipc = self.ipc_client = IpcClient(application_id)
            self.send_message = ipc.send_message
        except IpcClient.Error:
            ipc = self.ipc_server = IpcServer(application_id)
            ipc.handle_new_message = self.handle_new_message
        self.is_running = ipc.is_running

    def handle_new_message(self, message):
        print "Received:", message


if __name__ == "__main__":
    app = Application()
    if app.is_running:
        app.send_message(sys.argv)
    else:
        app.exec_()
