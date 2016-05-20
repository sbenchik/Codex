from PyQt4 import QtCore, QtGui, Qsci
from PyQt4.Qsci import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from lexerpygments import LexerPygments
import pygments
from pygments.formatters import NullFormatter
from pygments.styles import default
from pygments.lexers import TextLexer

filename = ""
font = QtGui.QFont("Ubuntu Mono", 12, 50)
lexer = pygments.lexers.TextLexer
s = "default"
f = NullFormatter(style=s)
from writerqsci import mainWindow
m = mainWindow()
