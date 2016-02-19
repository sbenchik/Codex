from PyQt4.QtCore import *
from PyQt4.QtGui import *


class GraphicsView(QGraphicsView):

    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)
        #QGraphicsView.RubberBandDrag)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setInteractive(True)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)

    def wheelEvent(self, event):
        factor = 1.41 ** (-event.delta() / 240.0)
        self.scale(factor, factor)

    def center(self):
        self.centerOn(self.width() / 2, self.height() / 2)

    def zoo_in(self):
        self.scale(1.25, 1.25)

    def zoom_out(self):
        self.scale(0.8, 0.8)

    def zoom(self, factor):
        self.resetMatrix()
        self.scale(factor, factor)

    def zoom_factor(self):
        return self.matrix().m11()


class GraphicsScene(QGraphicsScene):

    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)

    def delete_selected(self):
        for item in self.scene.selectedItems():
            self.scene.removeItem(item)

    def bring_to_front(self):
        if scene.selectedItems().isEmpty():
            return

        selectedItem = self.scene.selectedItems().first()
        overlapItems = selectedItem.collidingItems()

        zValue = 0
        for item in overlapItems:
            if (item.zValue() >= zValue and
                    isinstance(item, DiagramItem)):
                    zValue = item.zValue() + 0.1
        selectedItem.setZValue(zValue)

    def send_to_back(self):
        if scene.selectedItems().isEmpty():
            return

        selectedItem = self.scene.selectedItems().first()
        overlapItems = selectedItem.collidingItems()

        zValue = 0
        for item in overlapItems:
            if (item.zValue() <= zValue and
                    isinstance(item, DiagramItem)):
                    zValue = item.zValue() - 0.1
        selectedItem.setZValue(zValue)


class Editor(QWidget):

    def __init__(self, parent, width, height):
        QWidget.__init__(self, parent)
        self.hblayout = QHBoxLayout(self)
        self.view = GraphicsView(self)
        self.layout().addWidget(self.view)
        self.scene = GraphicsScene(self)
        self.scene.setSceneRect(0, 0, self.width(), self.height())
        self.view.setScene(self.scene)

        self.but = QLabel("test")  # QPushButton("Click me")
        item = self.scene.addWidget(self.but)
        item.setFlag(QGraphicsItem.ItemIsMovable)
        self.view.ensureVisible(item)

    def resizeEvent(self, event):
        self.view.center()
        return QWidget.resizeEvent(self, event)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = Editor(None, 800, 600)
    win.resize(640, 480)
    win.show()
    app.exec_()
