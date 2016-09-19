import sys
from PyQt5 import QtCore, QtWidgets, QtGui, Qsci
from PyQt5.QtGui import *

# Setting for no lexer. Taken from Baz Walter at
# https://riverbankcomputing.com/pipermail/pyqt/2009-July/023655.html

class QsciLexerText(Qsci.QsciLexerCustom):
    def __init__(self, parent=None):
        Qsci.QsciLexerCustom.__init__(self, parent)
        self._styles = {
        # There are not other styles because nothing else is needed in a
        # plain text lexer
             0: 'Default',
             }
        for key,value in self._styles.items():
            setattr(self, value, key)

    def description(self, style):
        return self._styles.get(style, '')

    def lexer(self):
        return "Plain Text"

    def defaultColor(self, style):
        if style == self.Default:
            return QtGui.QColor('#000000')
        return Qsci.QsciLexerCustom.defaultColor(self, style)

    def defaultFont(self, style):
        if style == self.Default:
            if sys.platform.startswith("linux"):
                return QFont("DejaVu Sans Mono", 10, 50)
            elif sys.platform.startswith("darwin"):
                return QFont("Menlo", 10, 50)
            elif sys.platform.startswith("win"):
                return QFont("Courier New", 10, 50)
        return Qsci.QsciLexerCustom.defaultFont(self, style)

    def styleText(self, start, end):
        editor = self.editor()
        if editor is None:
            return

         # scintilla works with encoded bytes, not decoded characters.
         # this matters if the source contains non-ascii characters and
         # a multi-byte encoding is used (e.g. utf-8)
        source = ''
        if end > editor.length():
            end = editor.length()
        if end > start:
            if sys.hexversion >= 0x02060000:
                 # faster when styling big files, but needs python 2.6
                source = bytearray(end - start)
                editor.SendScintilla(
                    editor.SCI_GETTEXTRANGE, start, end, source)
            else:
                source = unicode(editor.text()
                                ).encode('utf-8')[start:end]
        if not source:
            return

         # the line index will also be needed to implement folding
        index = editor.SendScintilla(editor.SCI_LINEFROMPOSITION, start)
        if index > 0:
             # the previous state may be needed for multi-line styling
            pos = editor.SendScintilla(
                    editor.SCI_GETLINEENDPOSITION, index - 1)
            state = editor.SendScintilla(editor.SCI_GETSTYLEAT, pos)
        else:
            state = self.Default

        set_style = self.setStyling
        self.startStyling(start, 0x1f)

        # scintilla always asks to style whole lines
        for line in source.splitlines(True):
            length = len(line)
            state = self.Default
            set_style(length, state)
            # folding implementation goes here
            index += 1
