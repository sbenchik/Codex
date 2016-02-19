# Based on http://stackoverflow.com/questions/6432656/highlight-a-scroll-bar
# TODO: look at https://freddie.witherden.org/tools/libqmarkedscrollbar/
import sys
from PyQt4 import QtCore, QtGui

class Annotation(object):
    
    # speed up attribute access
    __slots__ = ("start_pos", "end_pos", "color", "border_color", 
                 "tooltip", "on_click", "border_pen")

    def __init__(self, start_pos, end_pos, color, border_color=None, tooltip="", on_click=None):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = QtGui.QColor(color)
        self.border_color = border_color or self.color.darker()
        self.border_color.setAlphaF(0.4)
        self.border_pen = QtGui.QPen(self.border_color, 1.5)
        self.tooltip = tooltip
        self.on_click = on_click

class AnnotatedScrollBar(QtGui.QScrollBar):

    def __init__(self, annotations, parent=None):
        super(AnnotatedScrollBar, self).__init__(parent)
        # XXX: new KDE fusion style looks bad with this widget
        self.setStyle(QtGui.QStyleFactory.create('Plastique'))
        self.set_annotations(annotations)
        self.setMouseTracking(True)

    def set_annotations(self, annotations):
        self.annotations = annotations
        # rects are no atttributes of the Annotation instances to use the same
        # annotations for other views/scrollbars
        self.annotation_rects = [] 
        self.repaint()

    def clicked_annotation(self, pos):
        for i, rect in enumerate(self.annotation_rects):
            if rect.contains(pos):
                return self.annotations[i]

    def mouseMoveEvent(self, event):
        found = self.clicked_annotation(event.pos())
        if found is None:
            self.setCursor(QtCore.Qt.ArrowCursor)
            QtGui.QToolTip.hideText()
        else:
            self.setCursor(QtCore.Qt.PointingHandCursor)
            if found.tooltip:
                QtGui.QToolTip.showText(event.globalPos(), found.tooltip);
        return super(AnnotatedScrollBar, self).mouseMoveEvent(event)

    def mousePressEvent(self, event):
        found = self.clicked_annotation(event.pos())
        if found:
            self.setValue(found.start_pos)
            if found.on_click:
                found.on_click()
            return
        return super(AnnotatedScrollBar, self).mousePressEvent(event)

    def leaveEvent(self, event):
        self.unsetCursor()
        return super(AnnotatedScrollBar, self).leaveEvent(event)

    def resizeEvent(self, event):
        self.annotation_rects = []
        return super(AnnotatedScrollBar, self).resizeEvent(event)

    def recalc_annotations(self, rect):
        document_height = self.maximum()
        yscale = 1.0 / document_height
        x, y, w, h = rect
        self.annotation_rects = [QtCore.QRect(x, y + h * a.start_pos * yscale - 0.5,
                                  w, h * (a.end_pos - a.start_pos) * yscale + 1)
                                 for a in self.annotations]

    def paintEvent(self, event):
        super(AnnotatedScrollBar, self).paintEvent(event)
        
        p = QtGui.QPainter(self)
        opt = QtGui.QStyleOptionSlider()
        self.initStyleOption(opt)
        gr = self.style().subControlRect(QtGui.QStyle.CC_ScrollBar, opt,
                                         QtGui.QStyle.SC_ScrollBarGroove, self)
        sr = self.style().subControlRect(QtGui.QStyle.CC_ScrollBar, opt,
                                         QtGui.QStyle.SC_ScrollBarSlider, self)
        p.setClipRegion(QtGui.QRegion(gr) - QtGui.QRegion(sr), QtCore.Qt.IntersectClip)
        ar = self.annotation_rects
        if not ar:
            self.recalc_annotations(gr.getRect())
            ar = self.annotation_rects
        # speed ups
        set_brush = p.setBrush 
        set_pen = p.setPen
        draw_rect= p.drawRect
        for i, annotation in enumerate(self.annotations):
            set_brush(annotation.color)
            set_pen(annotation.border_pen)
            draw_rect(ar[i])


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    win = QtGui.QPlainTextEdit()
    win.setPlainText(open("scrollbar.py").read())
    win.resize(640, 500)
    def cb():
        print "test"
    sb = AnnotatedScrollBar([
        Annotation(5,6, "red", tooltip="red"),
        Annotation(15,16, "green", tooltip="green", on_click=cb),
        Annotation(16,17, "blue", tooltip="test"),
        ], win)
    win.setVerticalScrollBar(sb)
    win.show()
    app.exec_()