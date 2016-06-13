"""
File that contains global variables
"""

from PyQt4.Qsci import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from lexers.TextLexer import QsciLexerText
from theme import themeParser

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

THEMES = {
    "Default",
    "Oblivion"
}

filename = ""
theme = themeParser()
font = QFont("Ubuntu Mono", 12, 50)
lexer = QsciLexerText()
dark = False
from window import mainWindow
m = mainWindow()
