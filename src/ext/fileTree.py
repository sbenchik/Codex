"""
File tree widget. Currently major WIP.
"""

import os
import src.config
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class Tree(QWidget):
    def __init__(self, parent = None):
        super(Tree, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.fsModel = QtGui.QFileSystemModel()
        self.fsIndex = self.fsModel.setRootPath(QString(os.path.dirname(str(config.filename))))
        self.treeView = QtGui.QTreeView(self)
        self.treeView.setModel(self.fsModel)
        self.treeView.setRootIndex(self.fsIndex)
        self.treeView.setAnimated(True)
        self.treeView.setHeaderHidden(True)
        self.treeView.hideColumn(1)
        self.treeView.hideColumn(2)
        self.treeView.hideColumn(3)
        self.treeView.resize(150,430)
        #self.treeView.clicked.connect(self.clicked)

        # TODO: make this work so you can open files from the tree
    # def clicked(self):
    #     self.selModel = self.treeView.selectionModel()
    #     index = self.selModel.currentIndex()
    #     import runner
    #     with open(m.file,"rt") as f:
    #         runner.m.edit.setText(f.read())
    #         print "a"
    #         # Set the tab title to filename
    #         runner.m.tab.setTabText(runner.m.tab.currentIndex(),
    #                                    runner.m.FNToQString(runner.m.file))
