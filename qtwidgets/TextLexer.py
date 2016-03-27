import sys
from PyQt4 import QtCore, QtGui, Qsci
from PyQt4.QtGui import *

# Setting for no lexer. Taken from Baz Walter at
# https://riverbankcomputing.com/pipermail/pyqt/2009-July/023655.html

class QsciLexerText(Qsci.QsciLexerCustom):
    def __init__(self, parent=None):
        Qsci.QsciLexerCustom.__init__(self, parent)
        self._styles = {
             0: 'Default',
             # 1: 'Comment',
             # 2: 'Key',
             # 3: 'Assignment',
             # 4: 'Value',
             }
        for key,value in self._styles.iteritems():
            setattr(self, value, key)

    def description(self, style):
        return self._styles.get(style, '')

    def defaultColor(self, style):
        if style == self.Default:
            return QtGui.QColor('#000000')
         # elif style == self.Comment:
         #     return QtGui.QColor('#C0C0C0')
         # elif style == self.Key:
         #     return QtGui.QColor('#0000CC')
         # elif style == self.Assignment:
         #     return QtGui.QColor('#CC0000')
         # elif style == self.Value:
         #     return QtGui.QColor('#00CC00')
        return Qsci.QsciLexerCustom.defaultColor(self, style)

    def defaultFont(self, style):
        if style == self.Default:
            return QtGui.QFont("Mono", 10.5, QFont.Normal)
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
