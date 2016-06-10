from PyQt4.QtCore import QXmlStreamReader, QFile, QColor, QIODevice

class themeParser(QObject):
    """Parses XML theme files for use in editor class"""
    def __init__(self, arg):
        super(themeParser, self).__init__()
        file = QFile("/themes/"+theme+".xml")
        file.open(QIODevice.ReadOnly)

        self.types = QStringList()
        self.values = QStringList()

        self.reader = QXmlStreamReader(file)

    def defaultTheme(self):
        self.back = "#ffffff"
        self.fore = "#000000"
        self.hback = "#5294e2"
        self.hfore = "#ffffff"
        self.lnback = "#ffffff"
        self.lnfore = "#000000"
        self.cback = "#e6e6e6"

    def readTheme(self, theme):
        if not self.file.open(QFile.ReadOnly):
            defaultTheme()

        while not self.reader.isAtEnd():
            if self.reader.readNext() == QXmlStreamReader.startElement():
                if self.reader.name() == "type":
                    types.append(self.reader.readElementText())
                if self.reader.name() == "color":
                    values.append(self.reader.readElementText())

        self.reader.clear()
        file.close()

        if types.count() != values.count():
            defaultTheme()
        else:
            initTheme()

    def initTheme(self):
        self.back = values.at(types.indexOf("background"))
        self.fore = values.at(types.indexOf("foreground"))
        self.hback = values.at(types.indexOf("highlight_background"))
        self.hfore = values.at(types.indexOf("highlight_foreground"))
        self.lnback = values.at(types.indexOf("line_numbers_background"))
        self.lnfore = values.at(types.indexOf("line_numbers_foreground"))
        self.cback = values.at(types.indexOf("current_line_background"))

        self.others = values.at(types.indexOf("others"))
        self.numbers = values.at(types.indexOf("numbers"))
        self.strings = values.at(types.indexOf("strings"))
        self.keywords = values.at(types.indexOf("keywords"))
        self.comments = values.at(types.indexOf("comments"))
        self.functions = values.at(types.indexOf("functions"))

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

