from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QApplication, QSplitter, QLabel, QVBoxLayout

class MyWidget(QWidget):
    def __init__( self, parent = None ):
        super(MyWidget, self).__init__(parent)

        self.setMinimumWidth(400)
        self.setMinimumHeight(400)

        # create widgets
        a = QLabel('A' ,self)
        b = QLabel('B', self)
        c = QLabel('C', self)
        d = QLabel('D', self)

        for lbl in (a, b, c, d):
            lbl.setAlignment(Qt.AlignCenter)

        # create 2 horizontal splitters
        h_splitter1 = QSplitter(Qt.Horizontal, self)
        h_splitter1.addWidget(a)
        h_splitter1.addWidget(b)

        h_splitter2 = QSplitter(Qt.Horizontal, self)
        h_splitter2.addWidget(c)
        h_splitter2.addWidget(d)

        h_splitter1.splitterMoved.connect(self.moveSplitter)
        h_splitter2.splitterMoved.connect(self.moveSplitter)

        self._spltA = h_splitter1
        self._spltB = h_splitter2

        # create a vertical splitter
        v_splitter = QSplitter(Qt.Vertical, self)
        v_splitter.addWidget(h_splitter1)
        v_splitter.addWidget(h_splitter2)

        layout = QVBoxLayout()
        layout.addWidget(v_splitter)
        self.setLayout(layout)

    def moveSplitter( self, index, pos ):
        splt = self._spltA if self.sender() == self._spltB else self._spltB
        splt.blockSignals(True)
        splt.moveSplitter(index, pos)
        splt.blockSignals(False)

if ( __name__ == '__main__' ):
    app = QApplication([])
    widget = MyWidget()
    widget.show()
    app.exec_()
