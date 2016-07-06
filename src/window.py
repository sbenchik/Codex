"""
Class for the main window that contains tabs, editor, terminal, etc.
"""

import sys, os, cPickle, gzip, subprocess, config

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qsci import *

from ext.terminal import XTerm
from ext.find import Find
from ext.fileTree import Tree

from lexers.TextLexer import QsciLexerText
from Editor import Editor

class mainWindow(QtGui.QMainWindow):

    def __init__(self, parent = None):
        super(mainWindow, self).__init__(parent)
        config.filename = "Untitled"
        self.tabNum = 0
        self.treeVis = False
        self.termVis = False
        self.docList = []
        self.edit = Editor()
        self.editDict = {"edit1":self.edit}
        self.tab = QtGui.QTabWidget(self)

        self.initUI()

    def initActions(self):
        self.newAction = QtGui.QAction("New Window",self)
        self.newAction.setShortcut("Ctrl+N")
        self.newAction.triggered.connect(self.new)

        self.newTabAction = QtGui.QAction("New Tab",self)
        self.newTabAction.setShortcut("Ctrl+T")
        self.newTabAction.triggered.connect(self.newTab)

        self.openAction = QtGui.QAction("Open file",self)
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self.openFile)

        self.saveAction = QtGui.QAction("Save",self)
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.saveFile)

        self.saveasAction = QtGui.QAction("Save As",self)
        self.saveasAction.setShortcut("Ctrl+Shift+S")
        self.saveasAction.triggered.connect(self.saveFileAs)

        self.cutAction = QtGui.QAction("Cut",self)
        self.cutAction.setShortcut("Ctrl+X")
        self.cutAction.triggered.connect(lambda cut: self.edit.cut)

        self.copyAction = QtGui.QAction("Copy",self)
        self.copyAction.setShortcut("Ctrl+C")
        self.copyAction.triggered.connect(lambda copy: self.edit.copy)

        self.pasteAction = QtGui.QAction("Paste",self)
        self.pasteAction.setShortcut("Ctrl+V")
        self.pasteAction.triggered.connect(lambda paste: self.edit.paste)

        self.undoAction = QtGui.QAction("Undo",self)
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.triggered.connect(lambda undo: self.edit.undo)

        self.redoAction = QtGui.QAction("Redo",self)
        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.triggered.connect(lambda redo: self.edit.redo)

        self.aboutAction = QtGui.QAction("About Codex",self)
        self.aboutAction.triggered.connect(self.about)

        self.noLexAct = QtGui.QAction("Plain Text",self)
        self.noLexAct.triggered.connect(lambda noLex: self.edit.setLexer(QsciLexerText()))

        self.termAct = QtGui.QAction("Terminal",self)
        self.termAct.setCheckable(True)
        self.termAct.triggered.connect(self.toggleTerm)

        self.treeAct = QtGui.QAction("File Tree",self)
        self.treeAct.setCheckable(True)
        self.treeAct.triggered.connect(self.toggleTree)

        self.toggleIntAct = QtGui.QAction("Indentation Guides",self)
        self.toggleIntAct.triggered.connect(self.toggleIntGuide)
        self.toggleIntAct.setCheckable(True)
        self.toggleIntAct.setChecked(True)

        self.toggleLNAct = QtGui.QAction("Line Numbers",self)
        self.toggleLNAct.triggered.connect(self.toggleLN)
        self.toggleLNAct.setCheckable(True)
        self.toggleLNAct.setChecked(True)

        self.FRAct = QtGui.QAction("Find and Replace",self)
        self.FRAct.triggered.connect(self.fr)
        self.FRAct.setShortcut("Ctrl+F")

        self.fontAct = QtGui.QAction("Choose Font",self)
        self.fontAct.triggered.connect(self.chooseFont)

    def initMenubar(self):
        menubar = self.menuBar()

        file = menubar.addMenu("File")
        edit = menubar.addMenu("Edit")
        self.lang = menubar.addMenu("Languages")
        view = menubar.addMenu("View")
        about = menubar.addMenu("About")

        self.initLexers()

        file.addAction(self.newAction)
        file.addAction(self.newTabAction)
        file.addAction(self.openAction)
        file.addAction(self.saveAction)
        file.addAction(self.saveasAction)
        file.addSeparator()
        file.addAction(self.fontAct)

        edit.addAction(self.undoAction)
        edit.addAction(self.redoAction)
        edit.addSeparator()
        edit.addAction(self.copyAction)
        edit.addAction(self.cutAction)
        edit.addAction(self.pasteAction)
        edit.addAction(self.FRAct)

        view.addAction(self.termAct)
        view.addAction(self.toggleIntAct)
        view.addAction(self.toggleLNAct)
        view.addAction(self.treeAct)

        about.addAction(self.aboutAction)

    def lessTabs(self):
        self.tabNum = self.tabNum - 1
        self.docList.remove(self.docList[self.tab.currentIndex()+1])
        print self.docList
        if self.tabNum <= 1:
            self.tab.setTabsClosable(False)

    def initTabs(self):
        # Set up the tabs
        self.tab.tabCloseRequested.connect(self.tab.removeTab)
        self.tab.tabCloseRequested.connect(self.lessTabs)
        self.tab.setMovable(True)
        # Automatically make new tabs contain an editor widget
        self.tab.addTab(self.editDict.get("edit1"), config.filename)
        self.termSplit.addWidget(self.tab)


    def initUI(self):
        # Create first qsplitter for sidebar
        self.treeSplit = QSplitter()
        self.treeSplit.setOrientation(Qt.Horizontal)
        # Create second qsplitter (Allows split screen for terminal)
        self.termSplit = QSplitter()
        self.termSplit.setOrientation(Qt.Vertical)
        # Add a termSplit to the treeSplit
        self.treeSplit.addWidget(self.termSplit)
        self.setCentralWidget(self.treeSplit)
        # Create everything else
        self.initActions()
        self.initMenubar()
        self.initTabs()
        # Create terminal and widget
        self.term = XTerm(self)
        # x and y coordinates on the screen, width, height
        self.setGeometry(100,100,600,430)
        self.setWindowTitle("Codex")
        # Move up to the parent directory and set the window icons.
        # Without os.path it will look for icons in bin/
        self.setWindowIcon(QtGui.QIcon(os.path.join(
        os.path.dirname(os.path.dirname(__file__)))+ \
        "/icons/256x256/codex.png"))
        # Open any documents that were open before closing
        self.loadDocs()

    def initLexers(self):
        # Dict that maps lexer actions to their respective strings
        self.lexActs = {}
        langGrp = QActionGroup(self.lang)
        langGrp.setExclusive(True)
        self.lang.addAction(self.noLexAct)
        self.noLexAct.setCheckable(True)
        self.noLexAct.setChecked(True)
        self.noLexAct.setActionGroup(langGrp)
        self.lang.addSeparator()
        languages = sorted(config.LEXERS.keys())
        for i in languages:
            langAct = self.lang.addAction(i)
            langAct.setCheckable(True)
            langAct.setActionGroup(langGrp)
            self.lexActs[langAct] = i
        langGrp.triggered.connect(  \
            lambda lex: self.editDict.get("edit"+str(self.tab.currentIndex()+1)) \
            .setLang(self.lexActs.get(lex)))

    def new(self):
        main = mainWindow()
        main.show()

    def FNToQString(self, fn):
        return QString(os.path.basename(str(fn)))

    def open(self):
        index = self.tab.currentIndex()
        with open(self.file,"rt") as f:
            if self.tabNum >= 1:
                self.__newEditor()
                self.tab.setTabsClosable(True)
                self.tab.setTabText(index+1, self.FNToQString(self.file))
            if self.tabNum == 0:
                self.tabNum = 1
                self.tab.setTabText(index, self.FNToQString(self.file))
            # Set the tab title to filename
            #self.tab.setCurrentIndex(index + 1)
            self.editDict.get(("edit"+str(self.tabNum))).setText(f.read())
        # Not really sure where else to put this
        self.editDict.get("edit"+str(self.tab.currentIndex()+1)).setModified(False)
        self.editDict.get("edit"+str(self.tabNum)).textChanged.connect(self.unsaved)

    def __newEditor(self):
        self.tabNum+=1
        # Add a new entry to the dict and map it an editor object
        self.editDict["edit"+str(self.tabNum)] = Editor()
        print self.editDict
        print self.tabNum
        self.tab.addTab(self.editDict.get(("edit"+str(self.tabNum))),
                                          self.FNToQString(self.file))

    def openFile(self):
        self.file = QtGui.QFileDialog.getOpenFileName(self, 'Open File',".")
        print self.file
        try:
            self.docList.apppend(str(self.file))
            self.open()
        except AttributeError:
            self.open()
            # Add the filename to docList
            self.docList.append(str(self.file))
            print self.docList

    def loadDocs(self):
        fh = None
        if "No such file or directory" in \
        str(subprocess.Popen("find .open.p",shell=True).wait()):
            return
        else:
            try:
                fh = gzip.open(unicode(".open.p"), "rb")
                self.docList = cPickle.load(fh)
                print self.docList
                for x in self.docList:
                    self.file = x
                    self.open()
            except (IOError, OSError), e:
                print e
                return
            finally:
                if fh is not None:
                    fh.close()

    def save(self):
        # Save the file as plain text
        with open(self.docList[self.tab.currentIndex()], "wt") as file:
            file.write(self.editDict.get("edit"+str(self.tab.currentIndex()+1)).text())
        # Note that changes to the document are saved
        self.edit.setModified(False)
        # Set the tab title to filename
        self.tab.setTabText(self.tab.currentIndex(),
                            self.FNToQString(self.docList[self.tab.currentIndex()]))

    def saveDocs(self):
        try:
            fh = gzip.open(unicode(".open.p"), "wb")
            cPickle.dump(self.docList, fh, 2)
        except (IOError, OSError), e:
            raise e
        finally:
            if fh:
                fh.close()

    def saveFile(self):
        # Only open if it hasn't previously been saved
        if self.docList[self.tab.currentIndex()] == "Untitled":
            self.docList[self.tab.currentIndex()] = \
            QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        self.save()

    def saveFileAs(self):
        config.filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        self.save()

    def unsaved(self):
        if self.editDict.get("edit"+str(self.tab.currentIndex()+1)).isModified:
            self.tab.setTabText(self.tab.currentIndex(),
                                self.FNToQString(self.docList[self.tab.currentIndex()]+"*"))

    def about(self):
        QtGui.QMessageBox.about(self, "About Codex",
                                "<p>Codex is a basic text editor for code " \
                                "made with PyQt4 and QScintilla.</p>"
                                )

    def toggleTabs(self):
        state = self.tab.isVisible()
        self.tab.setVisible(not state)

    def newTab(self):
        self.__newEditor()
        self.tab.setTabsClosable(True)

    def showTerm(self):
        self.termVis = True
        self.termSplit.addWidget(self.term)
        self.term.show_term()

    def hideTerm(self):
        self.termVis = False
        self.term.hide()

    def toggleTerm(self):
        self.hideTerm() if self.termVis else self.showTerm()

    def showTree(self):
        self.ftree = Tree(self)
        self.treeVis = True
        self.ftree.resize(80,430)
        self.treeSplit.addWidget(self.ftree)
        self.ftree.show()

    def hideTree(self):
        self.treeVis = False
        self.ftree.close()

    def toggleTree(self):
        self.hideTree() if self.treeVis else self.showTree()

    def toggleIntGuide(self):
        state = self.edit.indentationGuides()
        self.edit.setIndentationGuides(not state)

    def toggleLN(self):
        state = self.edit.marginLineNumbers(0)
        self.edit.setMarginLineNumbers(0, not state)
        self.edit.setMarginWidth(0,0) if state == True else self.edit. \
                                setMarginWidth(0,self.edit.metrics.width("00000"))

    def fr(self):
        frwin = Find(self)
        frwin.show()

    def chooseFont(self):
        font, ok = QtGui.QFontDialog.getFont()
        if ok:
            config.font = font
            config.lexer.setFont(config.font, -1)

    # This method adapted from Peter Goldsborough's Writer.
    # Alerts the user if they are saving an edited file.
    def closeEvent(self,event):
        self.saveDocs()
        if not self.edit.isModified():
            event.accept()
        else:
            dialog = QtGui.QMessageBox(self)
            dialog.setIcon(QtGui.QMessageBox.Warning)
            dialog.setText(config.filename+" has unsaved changes.")
            dialog.setInformativeText("Do you want to save your changes?")
            dialog.setStandardButtons(QtGui.QMessageBox.Save |
                                  QtGui.QMessageBox.Cancel |
                                  QtGui.QMessageBox.Discard)
            dialog.setDefaultButton(QtGui.QMessageBox.Save)
            response = dialog.exec_()
            if response == QtGui.QMessageBox.Save:
                self.save()
            elif response == QtGui.QMessageBox.Discard:
                event.accept()
            else: event.ignore()
