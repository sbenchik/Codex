"""
File that contains global variables
"""
import sys
from PyQt5.Qsci import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from lexers.TextLexer import QsciLexerText

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
        'POV-Ray': QsciLexerPOV(),
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


docList = []
if sys.platform.startswith("linux"):
    font = QFont("DejaVu Sans Mono", 10, 50)
elif sys.platform.startswith("darwin"):
    font = QFont("Menlo", 10, 50)
elif sys.platform.startswith("win"):
    font = QFont("Courier New", 10, 50)
lexer = QsciLexerText()
proDir = ""
from window import mainWindow
m = mainWindow()
