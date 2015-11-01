import sys, os
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qsci import *

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
        'Javascript': QsciLexerJavaScript(),
        'Lua': QsciLexerLua(),
        'Makefile': QsciLexerMakefile(),
        'MATLAB': QsciLexerMatlab(),
        'Octave': QsciLexerOctave(),
        'Pascal': QsciLexerPascal(),
        'Perl': QsciLexerPerl(),
        'Postscript': QsciLexerPostScript(),
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

    """Reimplemanetation of the main QsciScintilla class to handle tabs"""
    def __init__(self, parent = None):
        super(Editor, self).__init__(parent)
        self.initUI()

    def setLang(self, lex):
        self.setLexer(self.getLexer(lex))
        # Setting the lexer resets the margin background to gray
        # so it has to be reset to white
        self.setMarginsBackgroundColor(QColor("White"))
        self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, 'Ubuntu Mono')

    def getLexer(self, lex):
        lexer = LEXERS.get(lex)
        # Workaround because setting a lexer would set
        # the background to black and the text to white
        lexer.setDefaultPaper(QColor("White"))
        lexer.setDefaultColor(QColor("Black"))
        return lexer

    def initUI(self):
        # Enable brace matching
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        # Enable line numbers
        font = QFont()
        metrics = QFontMetrics(font)
        self.setMarginWidth(0,metrics.width("00000"))
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("White"))
        # Current line has different color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#E6E6E6"))

class Main(QtGui.QMainWindow):

    """Main class that contains everything"""
    def __init__(self, parent = None):
        super(Main, self).__init__(parent)
        self.filename = "Untitled"

        self.initUI()
        self.initActions()

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

        self.hideTabAction = QtGui.QAction("Hide Tabs",self)
        self.hideTabAction.setCheckable(True)
        self.hideTabAction.triggered.connect(self.toggleTabs)

        self.addToolBarBreak()

    def initUI(self):

        self.initActions()
        self.initMenubar()
        # x and y coordinates on the screen, width, height
        self.setGeometry(100,100,600,430)
        # Self explanatory
        self.setWindowTitle("Writer")
        # Set window icon
        self.setWindowIcon(QtGui.QIcon("pencil.png"))
        # Set up the tabs
        self.tab = QtGui.QTabWidget(self)
        self.setCentralWidget(self.tab)
        self.tab.setTabsClosable(True)
        self.tab.tabCloseRequested.connect(self.tab.removeTab)
        self.tab.setMovable(True)
        self.edit = Editor()
        self.tab.addTab(self.edit, self.filename)

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

        view.addAction(self.hideTabAction)

        about.addAction(self.aboutAction)

    def initLexers(self):

        # Dict that maps lexer actions to their respective strings
        self.lexActs = {}
        langGrp = QActionGroup(self.lang)
        langGrp.setExclusive(True)
        for i in LEXERS:
            langAct = self.lang.addAction(i)
            langAct.setCheckable(True)
            langAct.setActionGroup(langGrp)
            self.lexActs[langAct] = i
        langGrp.triggered.connect(lambda lex: self.edit.setLang(self.lexActs.get(lex)))

    def formatFN(self, fn):
        fn = str(fn)
        fn = os.path.basename(fn)
        fn = QString(fn)
        return fn

    def new(self):
        self.tab.addTab(Editor(), "Untitled")

    def open(self):
        # Get file names and only show text files
        self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File',".")

        if self.filename:
            with open(self.filename,"rt") as file:
                self.text.setText(file.read())

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
        self.tab.setTabText(0, self.formatFN(self.filename))

    def saveAs(self):
        self.filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
         # Save the file as plain text
        with open(self.filename, "wt") as file:
            file.write(self.edit.text())
        # Note that changes to the document are saved
        self.edit.setModified(False)
        # Set the tab title to filename
        self.tab.setTabText(0, self.formatFN(self.filename))

    def about(self):
        QtGui.QMessageBox.about(self, "About Writer",
                                "<p> Writer is an all-purpose text editor " \
                                "written in Python and Qt4.</p>"
                                )

    def toggleTabs(self):
        state = self.tabbar.isVisible()
        self.tabbar.setVisible(not state)

    def newTab(self):
        self.tab.addTab(Editor(), self.filename)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    app.exec_()
