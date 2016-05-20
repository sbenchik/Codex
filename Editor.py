import sys, config
from PyQt4 import QtCore, QtGui, Qsci
from PyQt4.QtGui import *
from PyQt4.Qsci import *
from lexerpygments import LexerPygments

class Editor(QsciScintilla):
    """QScintilla widget used in the editor"""
    def __init__(self, parent = None):
        super(Editor, self).__init__(parent)
        self.lp = LexerPygments()
        self.initUI()

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
        self.metrics = QFontMetrics(config.font)
        self.setMarginWidth(0,self.metrics.width("00000"))
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("White"))
        # Current line has different color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#E6E6E6"))
        # Set autocompletion
        self.setAutoCompletionSource(QsciScintilla.AcsDocument)
        self.setAutoCompletionThreshold(4)
        # Guess the language to set a lexer
        config.lexer = self.lp.guessLexer()
        #self.setText(highlight(str(self.text()), config.lexer, config.f))
        # Set the font of the application to be a mono font
        #config.lexer.setFont(config.font)
