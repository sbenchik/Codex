# -*- coding: utf-8 -*-
import sys
import os

# sys.path.remove("/usr/lib/python2.7/site-packages")
#import faulthandler
# faulthandler.enable()
#from fakehttpd import install_fake_httpd

from PyQt4.QtCore import QByteArray, QObject, pyqtSlot, pyqtSignal, QTimer, SIGNAL, QVariant, QUrl, Qt
from PyQt4.QtGui import QApplication, QWidget, QVBoxLayout
from PyQt4.QtWebKit import QWebView, QWebSettings


DEBUG = True


class PythonWebKitBridge(QObject):

    instance = None

    def __init__(self, webview):
        QObject.__init__(self, webview)
        self.webview = webview
        self.setObjectName("python")
        self.is_ready = False
        self.queue = []
        self.webview.page().mainFrame().javaScriptWindowObjectCleared.connect(
            self.attach)
        self.attach()
        self.__class__.instance = self

    def execute(self, code, wait_ready=True):
        if not self.is_ready and wait_ready:
            self.queue.append(code)
        else:
            return self._execute(code)

    def _execute(self, code):
        def pydict(qd):
            d = {}
            for k, v in qd.items():
                d[unicode(k)] = v  # convert from QString
            return d

        try_code = """try { %s
        } catch(error) {
          alert("execution failed: " + error);
          result = {pyjs_exception: error}
          result
        }
        """ % code
        if DEBUG:
            print "executing:\n", code
        variant = self.webview.page().mainFrame().evaluateJavaScript(try_code)
        result = variant.toPyObject()
        if isinstance(result, dict):
            result = pydict(result)
            error = result.get("pyjs_exception")
            if error:
                error = pydict(error)
                for row_number, line in enumerate(code.splitlines()):
                    print "%3i: %s" % (row_number, line)
                for k, v in error.items():
                    print "%s: %s" % (k, v)
                raise RuntimeError(error)
        return result

    def attach(self):
        self.webview.page().mainFrame().addToJavaScriptWindowObject(
            self.objectName(), self)
        self._execute("""
           var new_log = function() {
                 var l = [];
                 for(var i=0; i<arguments.length; i++)
                   l.push(""+arguments[i]);
                 python.log(l);
                 try {
                   console.old_log.apply(console, arguments);
                 } catch(e) {}
           };
           if(console.old_log == undefined) {
              console.old_log = console.log;
              console.log = new_log;
           }
      
        """)

    @pyqtSlot("QStringList")
    def log(self, msglist):
        try:
            print "[LOG] ", unicode(msglist[0]).encode("utf-8") % [unicode(msg).encode("utf-8") for msg in msglist[1:]]
        except Exception:
            print "[LOG] ", " ".join(unicode(msg).encode("utf-8") for msg in msglist)

    ready = pyqtSignal()

    @pyqtSlot()
    def on_ready(self):
        self.is_ready = True
        self.ready.emit()
        if self.queue:
            for code in self.queue:
                self._execute(code)
            del self.queue[:]


class OpenLayersBridge(PythonWebKitBridge):

    click = pyqtSignal("int", "int", "float", "float")

    @pyqtSlot("int", "int", "float", "float")
    def on_mouse_clicked(self, x, y, lat, lon):
        self.click.emit(x, y, lat, lon)

    def pixels2coord(self, x, y):
        result = self.execute("""
          var lonlat = map.getLonLatFromViewPortPx({x:%s, y:%s});
          var pos = lonlat.clone();
          var newpos = pos.transform(                              
               map.getProjectionObject(),
               new OpenLayers.Projection("EPSG:4326")
                //new OpenLayers.Projection("EPSG:90913")
             );

          var result = {lat: newpos.lat, lon:newpos.lon};
          result;
        """ % (x, y))
        return result["lat"], result["lon"]


class LayerBase(object):
    js = ""
    defaults = {}
    args = ()

    def __init__(self, *args, **kwargs):
        for key, value in self.defaults.items():
            self.__dict__[key] = value
        for key, value in zip(self.args, args):
            self.__dict__[key] = value
        self.__dict__.update(kwargs)
        self.oid = str(id(self)).replace("-", "X")

    def create_js(self):
        js = self.js % self.__dict__
        return '''
        var layer_%(id)s = new %(js)s
        window.map.addLayer(layer_%(id)s);''' % {"js": js, "id": self.oid}

    __str__ = create_js


class GooglePhysicalLayer(LayerBase):
    args = ("name,")
    defaults = {"name": "Google Physical"}
    js = 'OpenLayers.Layer.Google("%(name)s", {type: google.maps.MapTypeId.TERRAIN})'


class GoogleStreetsLayer(LayerBase):
    args = ("name,")
    defaults = {"name": "Google Streets"}
    js = 'OpenLayers.Layer.Google("%(name)s", {numZoomLevels: 20})'


class GoogleHybridLayer(LayerBase):
    args = ("name,")
    defaults = {"name": "Google Hybrid"}
    js = 'OpenLayers.Layer.Google("%(name)s", {type: google.maps.MapTypeId.HYBRID, numZoomLevels: 20})'


class GoogleSatelliteLayer(LayerBase):
    args = ("name,")
    defaults = {"name": "Google Satellite"}
    js = 'OpenLayers.Layer.Google("%(name)s", {type: google.maps.MapTypeId.SATELLITE, numZoomLevels: 22})'


class VectorLayerBase(LayerBase):
    pass


class KmlLayer(VectorLayerBase):
    args = ("name", "url")
    js = '''OpenLayers.Layer.Vector(%(name)r, {
           projection: map.displayProjection,
           visibility: false,
           strategies: [new OpenLayers.Strategy.Fixed()],
                protocol: new OpenLayers.Protocol.HTTP({
                url: %(url)r, 
                format: new OpenLayers.Format.KML({extractStyles: true, extractAttributes: true})
           })
        })
    '''


class WmsLayer(LayerBase):
    args = ("name", "url", "layers")
    js = '''OpenLayers.Layer.WMS(%(name)r, %(url)r, {
             layers: %(layers)r, version: '1.3.0', transparent: true, srs: "EPSG:90913"},
                           { visibility: false, singleTile:
                           true,transitionEffect: 'resize', sphericalMercator: true, 
                           isBaseLayer: false, transparent: true,
                           opacity: 0.8
                           })
    '''


class BlueMarbleLayer(WmsLayer):
    defaults = {"name": "Sattelite", "url":
                "http://localhost:7000/map/wms/", "layers": "sat"}


class BordersLayer(WmsLayer):
    defaults = {"name": "Borders", "url":
                "http://localhost:7000/map/wms/", "layers": "topo"}


class OsmLayer(LayerBase):
    args = ("name", "url")
    defaults = {"name": "OpenStreetMap", "url":
                "http://192.168.56.162/tiles/${z}/${x}/${y}.png"}
    js = 'OpenLayers.Layer.OSM(%(name)r, %(url)r)'


class Marker(object):

    js = """
      var point = new OpenLayers.LonLat(%(lon)s, %(lat)s);
      var marker_%(oid)s = new OpenLayers.Marker(point);
      marker_%(oid)s.map = window.map;
      window.markers.addMarker(marker_%(oid)s);
    """

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.oid = str(id(self)).replace("-", "X")

    def create_js(self):
        return self.js % self.__dict__


class MapWidget(QWidget):

    def __init__(self, parent=None, lat=None, lon=None, zoom=None):
        super(MapWidget, self).__init__(parent)
        self._layout = QVBoxLayout(self)
        self.layout().setContentsMargins(0, 0, 0, 0)
        QWebSettings.globalSettings().setAttribute(
            QWebSettings.LocalContentCanAccessFileUrls, True)
        QWebSettings.globalSettings().setAttribute(
            QWebSettings.LocalContentCanAccessRemoteUrls, True)
        QWebSettings.globalSettings().setAttribute(
            QWebSettings.DeveloperExtrasEnabled, True)
        self.webview = QWebView(self)
        self.bridge = OpenLayersBridge(self.webview)
        self.bridge.click.connect(self.click)
        self.layout().addWidget(self.webview)
        QTimer.singleShot(0, lambda: self.init(lat, lon, zoom))
        self.click.connect(self.clicked)

    def pixel2coord(self, x, y):
        return self.bridge.pixels2coord(0, 0)

    def clicked(self, x, y, lat, lon):
        marker = Marker(lat, lon)
        self.add_marker(marker)

    click = pyqtSignal("int", "int", "float", "float")

    def init(self, lat, lon, zoom):
        # self.webview.load(QUrl("http://localhost.app/static/index.html"))
        # install_fake_httpd(self.webview)
        # self.webview.load(QUrl("http://localhost.app/static/index.html"))
        path = os.path.dirname(os.path.abspath(__file__))
        html = open(os.path.join(path, "static", "index.html")).read()
        if lon is not None:
            html = html.replace("var lon = 8.2;", "var lon = %s;" % lon)
        if lat is not None:
            html = html.replace("var lat = 53.166;", "var lat = %s;" % lat)
        if zoom is not None:
            html = html.replace("var zoom = 4;", "var zoom = %s;" % zoom)
        html = html.replace("http://localhost.app", "file://%s" % path)
        if DEBUG:
            open("debug.html", "w").write(html)

        self.webview.setHtml(html)

    def move_marker(self, lat, lon):
        pass

    def center(self):
        pass

    def set_center(self, lat, lon):
        pass

    def zoom(self, factor):
        pass

    def add_layer(self, layer):
        self.bridge.execute(layer.create_js())

    def add_marker(self, marker):
        self.bridge.execute(marker.create_js())


def main():
    app = QApplication(sys.argv)
    win = MapWidget(None)
    win.add_layer(GoogleStreetsLayer())
    win.add_layer(BlueMarbleLayer())
    win.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main() or 0)
