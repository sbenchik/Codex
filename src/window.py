"""
Class for the main window that contains tabs, editor, terminal, etc.
"""

import sys, os, atexit, functools
import config

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
        self.tabNum = 1

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
        self.saveAction.triggered.connect(self.save)

        self.saveasAction = QtGui.QAction("Save As",self)
        self.saveasAction.setShortcut("Ctrl+Shift+S")
        self.saveasAction.triggered.connect(self.saveAs)

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

        self.showTermAct = QtGui.QAction("Show Terminal",self)
        self.showTermAct.setShortcut("Ctrl+Shift+T")
        self.showTermAct.triggered.connect(self.showTerm)

        self.hideTermAct = QtGui.QAction("Hide Terminal",self)
        self.hideTermAct.setShortcut("Ctrl+Shift+H")
        self.hideTermAct.triggered.connect(self.hideTerm)

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

        self.treeAct = QtGui.QAction("Show File Tree",self)
        self.treeAct.triggered.connect(self.showTree)

        self.hideTreeAct = QtGui.QAction("Hide File Tree",self)
        self.hideTreeAct.triggered.connect(self.hideTree)

        self.fontAct = QtGui.QAction("Choose Font",self)
        self.fontAct.triggered.connect(self.chooseFont)

        self.darkAct = QtGui.QAction("Dark Mode",self)
        self.darkAct.triggered.connect(self.darkMode)

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

        view.addAction(self.showTermAct)
        view.addAction(self.hideTermAct)
        view.addAction(self.toggleIntAct)
        view.addAction(self.toggleLNAct)
        view.addAction(self.treeAct)
        view.addAction(self.hideTreeAct)
        view.addAction(self.darkAct)

        about.addAction(self.aboutAction)

    def lessTabs(self):
        self.tabNum = self.tabNum - 1
        if self.tabNum == 1:
            self.tab.setTabsClosable(False)

    def initTabs(self):
        # Set up the tabs
        self.tab = QtGui.QTabWidget(self)
        self.tab.tabCloseRequested.connect(self.tab.removeTab)
        self.tab.tabCloseRequested.connect(self.lessTabs)
        self.tab.setMovable(True)
        # Automatically make new tabs contain an editor widget
        self.edit = Editor()
        self.tab.addTab(self.edit, config.filename)
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
        # Create terminal widget
        self.term = XTerm(self)
        # x and y coordinates on the screen, width, height
        self.setGeometry(100,100,600,430)
        self.setWindowTitle("Codex")
        # Move up to the parent directory and set the window icons.
        # Without os.path it will look for icons in bin/
        self.setWindowIcon(QtGui.QIcon(os.path.join(
                                os.path.dirname(os.path.dirname(__file__)))+ \
                                "/icons/256x256/codex.png"))
        # Change the filename if there are unsaved changes
        self.edit.textChanged.connect(self.unsaved)


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
            lambda lex: self.edit.setLang(self.lexActs.get(lex)))

    def new(self):
        main = mainWindow()
        main.show()

    def FNToQString(self, fn):
        return QString(os.path.basename(str(fn)))

    def open(self):
        try:
            with open(self.file,"rt") as f:
                self.edit.setText(f.read())
                # Set the tab title to filename
                self.tab.setTabText(self.tab.currentIndex(), self.FNToQString(self.file))
                self.edit.setModified(False)
        except AttributeError:
            config.filename = self.file
            with open(self.file,"rt") as f:
                self.edit.setText(f.read())
                # Set the tab title to filename
                self.tab.setTabText(self.tab.currentIndex(), self.FNToQString(self.file))
                self.edit.setModified(False)

    def openFile(self):
        # Get file names and only show text files
        self.file = QtGui.QFileDialog.getOpenFileName(self, 'Open File',".")
        config.filename = str(self.file)
        self.open()

    def save(self):
        # Only open if it hasn't previously been saved
        if config.filename == "Untitled":
            config.filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        # Save the file as plain text
        with open(config.filename, "wt") as file:
            file.write(self.edit.text())
        # Note that changes to the document are saved
        self.edit.setModified(False)
        # Set the tab title to filename
        self.tab.setTabText(self.tab.currentIndex(), self.FNToQString(config.filename))

    def saveAs(self):
        config.filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
         # Save the file as plain text
        with open(config.filename, "wt") as file:
            file.write(self.edit.text())
        # Note that changes to the document are saved
        self.edit.setModified(False)
        # Set the tab title to filename
        self.tab.setTabText(self.tab.currentIndex(), self.FNToQString(config.filename))

    def unsaved(self):
        self.saved = False
        self.tab.setTabText(self.tab.currentIndex(), self.FNToQString(config.filename+"*"))

    def about(self):
        QtGui.QMessageBox.about(self, "About Codex",
                                "<p>Codex is a basic text editor for code " \
                                "made with PyQt4 and QScintilla.</p>"
                                )

    def toggleTabs(self):
        state = self.tab.isVisible()
        self.tab.setVisible(not state)

    def newTab(self):
        self.tab.addTab(Editor(), config.filename)
        self.tabNum+=1
        self.tab.setTabsClosable(True)

    def showTerm(self):
        self.termSplit.addWidget(self.term)
        self.term.show_term()

    def hideTerm(self):
        self.term.hide()

    def toggleIntGuide(self):
        state = self.edit.indentationGuides()
        self.edit.setIndentationGuides(not state)

    def toggleLN(self):
        state = self.edit.marginLineNumbers(0)
        self.edit.setMarginLineNumbers(0, not state)
        if state == True:
            self.edit.setMarginWidth(0,0)
        elif state == False:
            self.edit.setMarginWidth(0,self.edit.metrics.width("00000"))

    def fr(self):
        frwin = Find(self)
        frwin.show()

    def showTree(self):
        self.ftree = Tree(self)
        self.ftree.resize(80,430)
        self.treeSplit.addWidget(self.ftree)
        self.ftree.show()

    def hideTree(self):
        self.ftree.close()

    def chooseFont(self):
       config.font, ok = QtGui.QFontDialog.getFont()
       if ok:
            self.edit.setFont(config.font)

    # This method adapted from Peter Goldsborough's Writer
    def closeEvent(self,event):
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

    def darkMode(self):
        config.dark = True
        config.lexer.setPaper(QColor("#232323"))
        self.edit.setMarginsBackgroundColor(QColor("#232323"))
        self.edit.setFoldMarginColors(QColor("#232323"),QColor("#232323"))
        self.edit.setMarginsForegroundColor(QColor("White"))
        self.edit.setCaretLineBackgroundColor(QColor("#525252"))
        config.lexer.setColor(QColor("White"), 0)
