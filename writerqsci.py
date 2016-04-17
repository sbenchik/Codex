import sys, os, atexit, functools, config

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qsci import *

from x11.terminal import XTerm
from find import Find
from TextLexer import QsciLexerText
from fileTree import Tree

LEXERS = {
        'Bash': QsciLexerBash(),
        'Batch': QsciLexerBatch(),
        'C': QsciLexerCPP(),
        'CMake': QsciLexerCMake(),
        'C++': QsciLexerCPP(),
        'C#': QsciLexerCSharp(),
        'CSS': QsciLexerCSS(),
        'D': QsciLexerD(),
        'Diff': QsciLexerDiff(),
        'Fortran': QsciLexerFortran(),
        'Fortran77': QsciLexerFortran77(),
        'HTML': QsciLexerHTML(),
        'IDL': QsciLexerIDL(),
        'Java': QsciLexerJava(),
        'JavaScript': QsciLexerJavaScript(),
        'JSON': QsciLexerJavaScript(),
        'Lua': QsciLexerLua(),
        'Makefile': QsciLexerMakefile(),
        'MATLAB': QsciLexerMatlab(),
        'Octave': QsciLexerOctave(),
        'Pascal': QsciLexerPascal(),
        'Perl': QsciLexerPerl(),
        'PHP': QsciLexerHTML(),
        'PostScript': QsciLexerPostScript(),
        'POV': QsciLexerPOV(),
        'Properties': QsciLexerProperties(),
        'Python': QsciLexerPython(),
        'Ruby': QsciLexerRuby(),
        'Spice': QsciLexerSpice(),
        'SQL': QsciLexerSQL(),
        'TCL': QsciLexerTCL(),
        'TeX': QsciLexerTeX(),
        'Verilog': QsciLexerVerilog(),
        'VHDL': QsciLexerVHDL(),
        'XML': QsciLexerXML(),
        'YAML': QsciLexerYAML(),
    }

class Editor(QsciScintilla):
    """QScintilla widget used in the editor"""
    def __init__(self, parent = None):
        super(Editor, self).__init__(parent)
        self.initUI()

    def setLang(self, lex):
        lexer = self.getLexer(lex)
        lexer.setDefaultFont(self.font)
        self.setLexer(lexer)
        lexer.setFont(self.font, 1)
        # Setting the lexer resets the margin background to gray
        # so it has to be reset to white
        self.setMarginsBackgroundColor(QColor("White"))

    def getLexer(self, lex):
        lexer = LEXERS.get(lex)
        # Workaround because setting a lexer would set
        # the background to black and the text to white
        lexer.setDefaultPaper(QColor("White"))
        lexer.setDefaultColor(QColor("Black"))
        return lexer

    def initUI(self):
        # Enable auto indentation and set them to 4 spaces
        self.setAutoIndent(True)
        self.setIndentationWidth(4)
        self.setIndentationGuides(True)
        # Enable brace matching
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        # Enable code folding
        self.setFolding(QsciScintilla.BoxedTreeFoldStyle)
        self.setFoldMarginColors(QColor("White"),QColor("White"))
        # Set the font to black mono
        self.font = QtGui.QFont("Mono", 11, QFont.Normal)
        self.metrics = QFontMetrics(self.font)
        self.setMarginWidth(0,self.metrics.width("00000"))
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("White"))
        # Current line has different color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#E6E6E6"))
        # Set autocompletion
        self.setAutoCompletionSource(QsciScintilla.AcsDocument)
        self.setAutoCompletionThreshold(4)
        # Set the font of the application to be a mono font
        self.setFont(self.font)
        # Set the language to plain text by default
        self.setLexer(QsciLexerText())

class mainWindow(QtGui.QMainWindow):

    """Main class that contains everything"""
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

        self.aboutAction = QtGui.QAction("About Writer",self)
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
        self.setWindowTitle("QsciWriter")
        # Set window icon
        self.setWindowIcon(QtGui.QIcon("pencil.png"))
        # Change the title if the text gets changed
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
        for i in LEXERS:
            langAct = self.lang.addAction(i)
            langAct.setCheckable(True)
            langAct.setActionGroup(langGrp)
            self.lexActs[langAct] = i
        langGrp.triggered.connect(lambda lex: self.edit.setLang(self.lexActs.get(lex)))

    def new(self):
        main = Main()
        main.show()

    def FNToQString(self, fn):
        return QString(os.path.basename(str(fn)))

    def open(self):
        try:
            with open(self.file,"rt") as f:
                self.edit.setText(f.read())
                # Set the tab title to filename
                self.tab.setTabText(self.tab.currentIndex(), self.FNToQString(self.file))
        except AttributeError:
            config.filename = self.file
            with open(self.file,"rt") as f:
                self.edit.setText(f.read())
                # Set the tab title to filename
                self.tab.setTabText(self.tab.currentIndex(), self.FNToQString(self.file))

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
        self.tab.setTabText(self.tab.currentIndex(), self.FNToQString(config.filename+"*"))

    def about(self):
        QtGui.QMessageBox.about(self, "About QsciWriter",
                                "<p>QsciWriter is a text editor " \
                                "made with PyQt4 and QScintilla." \
                                " It is based off Peter Goldsborough's "
                                "Writer tutorial from binpress.com.</p>"
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
        self.term.resize(600, 50)
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
