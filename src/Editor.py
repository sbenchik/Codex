import sys, config, lexers
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qsci import *
from lexers.TextLexer import QsciLexerText

class Editor(QsciScintilla):
    """Implementation of the editor component for Codex"""
    def __init__(self, parent = None):
        super(Editor, self).__init__(parent)
        self.initUI()

    def setLang(self, lex):
        if lex in config.LEXERS:
            self.lexer = self.getLexer(lex)
        else:
            self.lexer = lex
        self.lexer.setDefaultFont(config.font)
        self.lexer.setDefaultColor(QColor("Black"))
        self.setLexer(self.lexer)
        # Setting the lexer resets the margin background to gray
        # so it has to be reset to white
        self.setMarginsBackgroundColor(QColor("White"))
        # Comments use a serifed font by default so
        # they have to be set to use the same font
        self.lexer.setFont(config.font, 1)

    def getLexer(self, lex):
        self.lexer = config.LEXERS.get(lex)
        # Workaround because setting a lexer would set
        # the background to black and the text to white
        self.lexer.setDefaultPaper(QColor("White"))
        self.lexer.setDefaultColor(QColor("Black"))
        return self.lexer

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
        if len(config.docList) == 0:
            self.setLang(config.lexer)
        # Set the language to plain text by default
        #self.setLexer(config.lexer)
        # Set the font of the application to be a mono font
        #config.lexer.setFont(config.font)
