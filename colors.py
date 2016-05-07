import sys
from PyQt4 import QtCore, QtGui, Qsci
from PyQt4.QtGui import *

class algol(Qsci.QsciLexerCustom):
    from writerqsci import mainWindow
    config.m.edit.lexer.setColor('#888888', 1)
