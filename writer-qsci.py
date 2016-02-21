import sys, os, atexit, functools
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qsci import *
from qtwidgets.x11.terminal import XTerm

class QsciLexerText(QsciLexerCustom):
    """Setting for no lexer"""
    def __init__(self, parent=None):
        super(QsciLexerText, self).__init__(parent)

LEXERS = {
        'BASH': QsciLexerBash(),
        'Batch': QsciLexerBatch(),
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
        'Lua': QsciLexerLua(),
        'Makefile': QsciLexerMakefile(),
        'MATLAB': QsciLexerMatlab(),
        'Octave': QsciLexerOctave(),
        'Pascal': QsciLexerPascal(),
        'Perl': QsciLexerPerl(),
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
        self.setLexer(lexer)
        # Setting the lexer resets the margin background to gray
        # so it has to be reset to white
        self.setMarginsBackgroundColor(QColor("White"))
        self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, 'Ubuntu Mono')

    def getLexer(self, lex):
        lexer = LEXERS.get(lex)
        # Workaround because setting a lexer would set
        # the background to black and the text to white
        if lex != QsciLexerText:
            lexer.setDefaultPaper(QColor("White"))
            lexer.setDefaultColor(QColor("Black"))
        return lexer

    def initUI(self):
        # Enable auto indentation
        self.setAutoIndent(True)
        self.setIndentationGuides(True)
        # Enable brace matching
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        # Enable code folding
        self.setFolding(QsciScintilla.BoxedTreeFoldStyle)
        self.setFoldMarginColors(QColor("White"),QColor("White"))
        # Enable line numbers
        font = QFont()
        metrics = QFontMetrics(font)
        self.setMarginWidth(0,metrics.width("00000"))
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("White"))
        # Current line has different color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#E6E6E6"))
        # Set autocompletion
        self.setAutoCompletionSource(QsciScintilla.AcsDocument)
        self.setAutoCompletionThreshold(4)

class Main(QtGui.QMainWindow):

    """Main class that contains everything"""
    def __init__(self, parent = None):
        super(Main, self).__init__(parent)
        self.filename = "Untitled"
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
        self.openAction.triggered.connect(self.open)

        self.saveAction = QtGui.QAction("Save",self)
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.save)

        self.saveasAction = QtGui.QAction("Save As",self)
        self.saveasAction.setShortcut("Ctrl+Shift+S")
        self.saveasAction.triggered.connect(self.saveAs)

        self.aboutAction = QtGui.QAction("About Writer",self)
        self.aboutAction.triggered.connect(self.about)

        self.noLexAct = QtGui.QAction("Plain Text",self)
        self.noLexAct.triggered.connect(lambda noLex: self.edit.setLang(QsciLexerText))

        self.showTermAct = QtGui.QAction("Show Terminal",self)
        self.showTermAct.setShortcut("Ctrl+Shift+T")
        self.showTermAct.triggered.connect(self.showTerm)

        self.hideTermAct = QtGui.QAction("Hide Terminal",self)
        self.hideTermAct.setShortcut("Ctrl+Shift+H")
        self.hideTermAct.triggered.connect(self.hideTerm)

        self.addAct = QtGui.QAction("Add brace",self)
        self.addAct.triggered.connect(self.addBrace)

    def initUI(self):
        # Create qsplitter (Allows split screen for terminal)
        self.split = QSplitter()
        self.split.setOrientation(Qt.Vertical)
        self.setCentralWidget(self.split)
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
        self.tab.addTab(self.edit, self.filename)
        self.split.addWidget(self.tab)
        self.addBrace()

    def initMenubar(self):

        menubar = self.menuBar()

        file = menubar.addMenu("File")
        edit = menubar.addMenu("Edit")
        doc = menubar.addMenu("Document")
        self.lang = doc.addMenu("Languages")
        view = menubar.addMenu("View")
        about = menubar.addMenu("About")

        self.initLexers()

        file.addAction(self.newAction)
        file.addAction(self.newTabAction)
        file.addAction(self.openAction)
        file.addAction(self.saveAction)
        file.addAction(self.saveasAction)
        file.addAction(self.addAct)

        view.addAction(self.showTermAct)
        view.addAction(self.hideTermAct)

        about.addAction(self.aboutAction)

    def initLexers(self):
        # Dict that maps lexer actions to their respective strings
        self.lexActs = {}
        langGrp = QActionGroup(self.lang)
        langGrp.setExclusive(True)
        self.lang.addAction(self.noLexAct)
        self.noLexAct.setCheckable(True)
        self.noLexAct.setActionGroup(langGrp)
        self.lang.addSeparator()
        for i in LEXERS:
            langAct = self.lang.addAction(i)
            langAct.setCheckable(True)
            langAct.setActionGroup(langGrp)
            self.lexActs[langAct] = i
        langGrp.triggered.connect(lambda lex: self.edit.setLang(self.lexActs.get(lex)))

    def FNToQString(self, fn):
        return QString(os.path.basename(str(fn)))

    def new(self):
        main = Main()
        main.show()

    def open(self):
        # Get file names and only show text files
        self.file = QtGui.QFileDialog.getOpenFileName(self, 'Open File',".")
        if self.file:
            with open(self.file,"rt") as f:
                self.edit.setText(f.read())
                # Set the tab title to filename
                self.tab.setTabText(self.tab.currentIndex(), self.FNToQString(self.file))
                self.filename = str(self.file)

    def save(self):
        # Only open if it hasn't previously been saved
        if self.filename == "Untitled":
            self.filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        # Save the file as plain text
        with open(self.filename, "wt") as file:
            file.write(self.edit.text())
        # Note that changes to the document are saved
        self.edit.setModified(False)
        # Set the tab title to filename
        self.tab.setTabText(self.tab.currentIndex(), self.FNToQString(self.filename))

    def saveAs(self):
        self.filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
         # Save the file as plain text
        with open(self.filename, "wt") as file:
            file.write(self.edit.text())
        # Note that changes to the document are saved
        self.edit.setModified(False)
        # Set the tab title to filename
        self.tab.setTabText(self.tab.currentIndex(), self.FNToQString(self.filename))

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
        self.tab.addTab(Editor(), self.filename)
        self.tabNum+=1
        self.tab.setTabsClosable(True)

    def showTerm(self):
        self.split.addWidget(self.term)
        self.term.resize(600, 50)
        self.term.show_term()

    def hideTerm(self):
        self.term.hide()

    def addBrace(self):
        # if self.edit.wordAtLineIndex(self.edit.lines(), self.edit.length()-1) == QString("{"):
        #     self.edit.insert(QString("}"))
        print str(self.edit.wordAtLineIndex(1,26))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    app.exec_()
