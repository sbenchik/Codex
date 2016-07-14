import sys, os
os.sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class Tree(QWidget):
    """ File tree widget for Codex"""
    def __init__(self, parent = None):
        super(Tree, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.fsModel = QtGui.QFileSystemModel()
        self.sModel = QtGui.QItemSelectionModel(self.fsModel)
        # If the user entered a project directory, use that.
        # If not, go two levels up from the current file
        if config.proDir is not "":
            self.fsIndex = self.fsModel.setRootPath(config.proDir)
        else:
            self.fsIndex = self.fsModel.setRootPath(QString( \
                                        os.path.dirname(os.path.dirname( \
                                                        config.docList \
                                                        [config.m.tab.currentIndex()]))))
        self.treeView = QtGui.QTreeView(self)
        self.treeView.setModel(self.fsModel)
        self.treeView.setDragEnabled(True)
        self.treeView.setDragDropMode(QAbstractItemView.InternalMove)
        self.treeView.setRootIndex(self.fsIndex)
        self.treeView.setAnimated(True)
        self.treeView.setHeaderHidden(True)
        self.treeView.hideColumn(1)
        self.treeView.hideColumn(2)
        self.treeView.hideColumn(3)
        self.treeView.resize(150,430)
        self.treeView.clicked.connect(self.clicked)

    def clicked(self):
        print self.sModel.selectedIndexes()
        config.m.file = self.fsModel.filePath(self.fsModel.index(
                                            self.sModel.selectedIndexes()))
        print config.m.file
        try:
            config.docList.apppend(str(self.file))
            config.m.open()
        except AttributeError:
            config.m.open()
            # Add the filename to docList
            config.docList.append(str(self.file))
            print config.docList
