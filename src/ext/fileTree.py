import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
        self.treeView.setSelectionModel(self.sModel)
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
        config.m.file = self.fsModel.filePath(self.sModel.selectedIndexes()[0])
        try:
            config.docList.apppend(str(config.m.file))
            #print config.docList
            config.m.open()
        except AttributeError:
            config.docList.append(str(config.m.file))
            config.m.open()
            #print config.docList
