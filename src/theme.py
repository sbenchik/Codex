from PyQt4.QtCore import QObject, QXmlStreamReader, QFile, QIODevice
from PyQt4.QtGui import QColor

class themeParser(QObject):
    """Parses XML theme files for use in editor class.
    This code comes from Alex Spataru's Thunderpad and was
    adapted for Codex. """
    def __init__(self, parent=None):
        super(themeParser, self).__init__()

        self.types = {}
        self.colors = {}

    def defaultTheme(self):
        self.back = "#ffffff"
        self.fore = "#000000"
        self.hback = "#5294e2"
        self.hfore = "#ffffff"
        self.lnback = "#ffffff"
        self.lnfore = "#000000"
        self.cback = "#e6e6e6"

    def readTheme(self, theme):
        file = QFile("/themes/"+theme+".xml")
        file.open(QIODevice.ReadOnly)

        self.reader = QXmlStreamReader(file)

        if not self.file.open(QFile.ReadOnly):
            defaultTheme()

        while not self.reader.isAtEnd():
            if self.reader.readNext() == QXmlStreamReader.StartElement():
                if self.reader.name() == "type":
                    types.append(self.reader.readElementText())
                if self.reader.name() == "color":
                    colors.append(self.reader.readElementText())

        self.reader.clear()
        file.close()

        if types.count() != colors.count():
            defaultTheme()
        else:
            initTheme()

    def initTheme(self):
        self.back = colors.at(types.indexOf("background"))
        self.fore = colors.at(types.indexOf("foreground"))
        self.hback = colors.at(types.indexOf("highlight_background"))
        self.hfore = colors.at(types.indexOf("highlight_foreground"))
        self.lnback = colors.at(types.indexOf("line_numbers_background"))
        self.lnfore = colors.at(types.indexOf("line_numbers_foreground"))
        self.cback = colors.at(types.indexOf("current_line_background"))

        self.others = colors.at(types.indexOf("others"))
        self.numbers = colors.at(types.indexOf("numbers"))
        self.strings = colors.at(types.indexOf("strings"))
        self.keywords = colors.at(types.indexOf("keywords"))
        self.comments = colors.at(types.indexOf("comments"))
        self.functions = colors.at(types.indexOf("functions"))

    # These return all of the components of the theme as QColors

    def back(self):
        return QColor(self.back)

    def fore(self):
        return QColor(self.fore)

    def hback(self):
        return QColor(self.hback)

    def hfore(self):
        return QColor(self.hfore)

    def lnback(self):
        return QColor(self.lnback)

    def lnfore(self):
        return QColor(self.lnfore)

    def cback(self):
        return QColor(self.cback)

    def others(self):
        return QColor(self.others)

    def numbers(self):
        return QColor(self.numbers)

    def strings(self):
        return QColor(self.strings)

    def keywords(self):
        return QColor(self.keywords)

    def comments(self):
        return QColor(self.comments)

    def functions(self):
        return QColor(self.functions)

