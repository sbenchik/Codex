# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class ListModel(QAbstractListModel):

    def __init__(self, items):
        QAbstractListModel.__init__(self)
        self.items = items

    def append(self, item):
        self.items.append(item)

    def extend(self, items):
        self.items.extend(items)

    def __len__(self):
        return len(self.items)

    def data(self, index, role):
        if index.isValid() and role in (Qt.DisplayRole, Qt.EditRole):
            return QVariant(self.items[index.row()])
        else:
            return QVariant()

    def rowCount(self, parent=QModelIndex()):
        return len(self)


# from ktoon/widgetlistview.cpp
class WidgetList(QTableWidget):

    def __init__(self, parent=None):
        QTableWidget.__init__(self, 0, 1, parent)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.verticalHeader().hide()
        self.horizontalHeader().hide()
        self.horizontalHeader().setResizeMode(QHeaderView.Custom)
        # self.horizontalHeader().setStretchLastSection(True)
        self.items = {}
        self.connect(
            self, SIGNAL("clicked(const QModelIndex&)"), self.on_clicked)
        self.old = None

    def keyPressEvent(self, event):
        res = QTableWidget.keyPressEvent(self, event)
        self.on_clicked(self.currentIndex())
        return res

    def on_clicked(self, index):
        widget = self.indexWidget(index)
        if not widget:
            return
        if self.old:
            self.old.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        widget.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.old = widget
        self.emit(SIGNAL("widget_clicked"), widget)

    def add_widget(self, widget):
        return self.insert_widget(self.rowCount(), widget)

    def insert_widget(self, pos, widget):
        widget.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        item = QTableWidgetItem()
        self.insertRow(pos)
        self.setItem(pos, 0, item)
        self.setIndexWidget(self.indexFromItem(item), widget)
        self.verticalHeader().resizeSection(pos, widget.height())
        self.items[widget] = item
        widget.setMinimumHeight(widget.height())
        widget.installEventFilter(self)
        return item

    def eventFilter(self, widget, event):
        if isinstance(event, QResizeEvent):
            item = self.item(widget)
            index = self.indexFromItem(item)
            self.verticalHeader().resizeSection(index.row(), widget.height())
        return False

    def widget(self, item):
        return self.indexWidget(self.indexFromItem(item))

    def item(self, widget):
        return self.items[widget]

    def resizeEvent(self, event):
        self.horizontalHeader().resizeSection(0, event.size().width())

    def move_item_up(self, index):
        if index > 0:
            self.verticalHeader().moveSection(index, index - 1)

    def move_item_down(self, index):
        if index < self.rowCount():
            self.verticalHeader().moveSection(index, index + 1)

    def current_row_index(self):
        return self.verticalHeader().visualIndex(self.currentRow())
