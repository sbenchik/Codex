"""
Implementation of the editor component for Codex
"""

import sys, config, lexers
from PyQt4 import QtCore, QtGui, Qsci
from PyQt4.QtGui import *
from PyQt4.Qsci import *
from lexers.TextLexer import QsciLexerText
from lexers.lexerpygments import LexerPygments

class Editor(QsciScintilla):
    def __init__(self, parent = None):
        super(Editor, self).__init__(parent)
        self.initUI()

    def setLang(self, lex):
        config.lexer = lexers.getLexer(lex)
        config.lexer.setDefaultFont(config.font)
        self.setLexer(config.lexer)
        # Setting the lexer resets the margin background to gray
        # so it has to be reset to white
        self.setMarginsBackgroundColor(QColor("White"))
        # Comments use a different font by default so
        # they have to be set to use the same font
        config.lexer.setFont(config.font, 1)
        if config.dark:
            # Setting a new lexer undoes some dark mode settings, so dark mode
            # has to be reset
            config.m.darkMode()
            config.lexer.setColor(QColor("White"))

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
        # Set the language to plain text by default
        self.setLexer(config.lexer)
        # Set the font of the application to be a mono font
        config.lexer.setFont(config.font)

    # These three methods are taken from eric 6 and are needed for the
    # Pygments lexer
    def startStyling(self, pos, mask):
        self.SendScintilla(QsciScintilla.SCI_STARTSTYLING, pos, mask)

    def setStyling(self, length, style):
        self.SendScintilla(QsciScintilla.SCI_SETSTYLING, length, style)

    def getLineSeparator(self):
        m = self.eolMode()
        if m == QsciScintilla.EolWindows:
             eol = '\r\n'
        elif m == QsciScintilla.EolUnix:
            eol = '\n'
        elif m == QsciScintilla.EolMac:
           eol = '\r'
        else:
           eol = ''
        return eol
