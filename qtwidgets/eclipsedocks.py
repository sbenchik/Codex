from PyQt4.QtCore import *
from PyQt4.QtGui import *


class TitleTab(QTabBar):

    def __init__(self, parent):
        QTabBar.__init__(self, parent)
        font = self.font()
        pt = font.pointSize() * 0.75
        font.setPointSize(pt)
        self.setFont(font)
        # self.setShape(QTabBar.TriangularNorth)
        self.setProperty("documentMode", QVariant(True))
        self.setProperty("tabsClosable", QVariant(True))
        #self.setProperty("movable", QVariant(True))

    def mousePressEvent(self, event):
        QTabBar.mousePressEvent(self, event)
        if not (event.buttons() & Qt.LeftButton):
            return
        self.start_pos = QPoint(event.pos())
        self.detached = False
        self.parent().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        QTabBar.mouseReleaseEvent(self, event)
        self.parent().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        QTabBar.mouseMoveEvent(self, event)
        if not (event.buttons() & Qt.LeftButton):
            return
        if not self.parent().rect().contains(event.pos()):
            if self.detached:
                return
            detached = True
            self.parent().parent().detach()
            self.parent().mouseMoveEvent(event)


class TitleButton(QToolButton):

    def __init__(self, parent, icon_name, callback):
        QToolButton.__init__(self, parent)
        self.setFixedSize(16, 16)
        self.setAutoRaise(True)
        self.setIcon(QIcon(icon_name))
        self.setCheckable(True)
        self.connect(self, SIGNAL("clicked()"), callback)


class TitleBarWidget(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)

        import eclipsedocks_icons

        self.setObjectName("titlebar")
        self._hblayout = QHBoxLayout(self)
        self._tab = TitleTab(self)
        self._pinButton = TitleButton(
            self, ":pin.png", self.parent().toggle_autohide)
        self._minimizeButton = TitleButton(
            self, ":minimize.png", self.parent().toggle_minimize)
        self._maximizeButton = TitleButton(
            self, ":maximize.png", self.parent().toggle_maximize)
        self.layout().setMargin(1)
        self.layout().setSpacing(0)
        self.layout().addWidget(self._tab)
        # self.layout().addStretch()
        self.layout().addWidget(self._pinButton)
        self.layout().addWidget(self._minimizeButton)
        self.layout().addWidget(self._maximizeButton)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(event.rect(), QBrush(QColor("#1010ff")))
        QWidget.paintEvent(self, event)


class DockWidgetContainer(QDockWidget):

    def __init__(self, parent=None):
        QDockWidget.__init__(self, parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout().setMargin(0)
        self.layout().setSpacing(0)
        self._orig_title_bar = self.titleBarWidget()
        self._title_bar = TitleBarWidget(self)
        self._tab = self._title_bar._tab
        self.setTitleBarWidget(self._title_bar)
        self._stack = QStackedWidget(self)
        self.setWidget(self._stack)
        self._widgets = []
        self._docks = []
        self.entered = False
        self.pinned = True
        self.shot = False

        self.connect(
            self._tab, SIGNAL("currentChanged(int)"),
            self.on_tab_changed)
        self.connect(
            self._tab, SIGNAL("tabCloseRequested(int)"),
            self.close_tab)
        self.connect(
            self, SIGNAL("topLevelChanged(bool)"),
            self.test_tabify)
        self.connect(
            self, SIGNAL("dockLocationChanged(Qt::DockWidgetArea)"),
            self.on_area_changed)

    def close_tab(self, idx):
        widget = self._widgets[idx]
        self._stack.removeWidget(widget)
        self._tab.removeTab(idx)
        del self._widgets[idx]
        if not self._widgets:
            self.parent().removeDockWidget(self)

    def minimumSizeHint(self):
        return self._title_bar.sizeHint()

    def on_tab_changed(self, idx):
        self._stack.setCurrentIndex(idx)
        # self.setWindowTitle(self._widgets[idx].windowTitle())

    def add_widget(self, widget):
        widget.setParent(self._stack)
        self._stack.addWidget(widget)
        self._widgets.append(widget)
        self._tab.addTab(widget.windowTitle())
        widget.show()

    def detach(self):
        sel = self._tab.currentIndex()
        count = self._tab.count()
        if count == 1:
            return

        dock = self.__class__(self.parent())
        self.parent().addDockWidget(self.area, dock)
        dock.show()

        for i in range(count - 1, -1, -1):
            if i == sel:
                continue
            self._tab.removeTab(i)
            widget = self._widgets[i]
            del self._widgets[i]
            self._stack.removeWidget(widget)
            dock.add_widget(widget)
        self._docks.append(dock)

    def on_area_changed(self, area):
        self.area = area

    def test_tabify(self, flag):
        tabbed_docks = self.parent().tabifiedDockWidgets(self)
        if not len(tabbed_docks):
            return
        for dock in tabbed_docks:
            for widget in dock._widgets:
                dock._stack.removeWidget(widget)
                self.add_widget(widget)
            self.parent().removeDockWidget(dock)

    def toggle_autohide(self):
        state = self.sender().isChecked()
        self.pinned = state

    def toggle_minimize(self):
        state = self.sender().isChecked()
        self.setCollapsed(not state)

    def setCollapsed(self, state):
        self._stack.setVisible(state)

    def toggle_maximize(self):
        state = self.sender().isChecked()
        if state:
            self._stack.resize(self._stack.maximumSize())
        else:
            self._stack.resize(self._stack.sizeHint())

    def enterEvent(self, event):
        self.entered = True
        if not self.shot and not self.pinned and not self.isFloating():
            self.shot = True
            QTimer.singleShot(500, self.autoshow)
        return QDockWidget.enterEvent(self, event)

    def leaveEvent(self, event):
        self.entered = False
        if not self.shot and not self.pinned and not self.isFloating():
            self.shot = True
            QTimer.singleShot(1000, self.autohide)
        return QDockWidget.leaveEvent(self, event)

    def autohide(self):
        self.shot = False
        if not self.entered:
            self.setCollapsed(False)

    def autoshow(self):
        self.shot = False
        if self.entered:
            self.setCollapsed(True)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv + ["-style", "plastique"])
    win = QMainWindow()
    try:
        win.setTabPosition(Qt.LeftDockWidgetArea, QTabWidget.North)
        win.setTabPosition(Qt.RightDockWidgetArea, QTabWidget.North)
        win.setTabPosition(Qt.TopDockWidgetArea, QTabWidget.North)
        win.setTabPosition(Qt.BottomDockWidgetArea, QTabWidget.North)
    except AttributeError:
        pass
    c = QLabel(win)
    c.setStyleSheet("* { background: gray }")
    win.setCentralWidget(c)
    win.resize(640, 480)
    dock_container1 = DockWidgetContainer(win)
    dock1 = QLabel("Test 1")
    dock1.setWindowTitle(dock1.text())
    dock2 = QPushButton("Test 2")
    dock2.setWindowTitle(dock2.text())
    dock_container1.add_widget(dock1)
    dock_container1.add_widget(dock2)
    win.addDockWidget(Qt.LeftDockWidgetArea, dock_container1)

    dock_container2 = DockWidgetContainer(win)
    dock3 = QPushButton("Test 3")
    dock3.setWindowTitle(dock3.text())
    dock_container2.add_widget(dock3)
    win.addDockWidget(Qt.RightDockWidgetArea, dock_container2)

    win.show()
    app.exec_()
