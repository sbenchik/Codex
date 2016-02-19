# -*- coding: utf-8 -*-
import __main__
import os
from ConfigParser import SafeConfigParser as IniFile

try:
    from elementtree.ElementTree import ElementTree
except ImportError:
    try:
        from xml.etree.ElementTree import ElementTree
    except ImportError:
        ElementTree = None


__all__ = [
    "Fallback", "Kde", "Gnome", "DesktopEnvironment", "detect_environment", "find_icon",
]

_exists = {}


def path_exists(name):
    try:
        flag = _exists[name]
    except KeyError:
        flag = os.path.exists(name)
        _exists[name] = flag
    return flag

path_join = os.path.join
dir_name = os.path.dirname
base_name = os.path.basename
abs_path = os.path.abspath
expand_user = os.path.expanduser
get_env = os.environ.get


class DesktopEnvironment(object):

    def __new__(cls, *args):
        # Singleton
        if not '_instance' in cls.__dict__:
            cls._instance = {}
        instance = cls._instance.get((args,))
        if not instance:
            instance = object.__new__(cls, *args)
            cls._instance[(args,)] = instance
        return instance

    def __init__(self, application_name=None):
        main_filename = abs_path(__main__.__file__)
        application_prefix = dir_name(main_filename)
        self.application_name = application_name or base_name(main_filename)
        if base_name(application_prefix) in ("bin", "sbin"):
            application_prefix = dir_name(application_prefix)

        self.icon_theme_search_path = [
            "/usr/share/icons",
            "/usr/local/share/icons",
            expand_user(path_join("~", ".local", "share", "icons")),
        ]

        self.icon_search_path = [
            path_join(application_prefix, "share",
                      "apps", self.application_name, "icons"),
            path_join(application_prefix, "icons"),
            path_join(application_prefix, "share", "icons"),
            expand_user(
                path_join(
                    "~", ".local", "share", "apps", self.application_name, "icons")),
            expand_user(path_join("~", "." + self.application_name, "icons")),
            expand_user(
                path_join("~", "." + self.application_name, "share", "icons")),
            expand_user(
                path_join(
                    os.sep, "usr", "local", "share", "apps", self.application_name, "icons")),
        ]
        self.icons = []
        self.init()

        # Find theme
        found = []
        current_icon_theme = self.current_icon_theme()

        while True:
            theme = self.read_icon_theme(current_icon_theme)
            if theme:
                path, inherits = theme
                if path in found:
                    break
                if path_exists(path):
                    found.append(path)
                    if not inherits:
                        break
                    current_icon_theme = inherits
                else:
                    break
            else:
                break

        for path in reversed(found):
            for size in reversed(["22x22", "32x32", "48x48", "64x64", "128x128"]):
                self.icon_search_path.insert(0, path_join(path, size))

        # Remove non-existing and double paths
        found = []
        for path in self.icon_search_path:
            if path in found:
                continue
            if not path_exists(path):
                continue
            found.append(path)
        self.icon_search_path = found

    def read_icon_theme(self, theme_name):
        for path in self.icon_theme_search_path:
            theme_path = path_join(path, theme_name)
            filename = path_join(theme_path, "index.theme")
            if not path_exists(filename):
                continue
            cfg = IniFile()
            try:
                cfg.read([filename])
            except Exception, e:
                continue
            try:
                inherits = cfg.get("Icon Theme", "Inherits")
            except:
                inherits = None
            return theme_path, inherits

    def init(self):
        pass

    def find(self, name, size=None):
        if not name.endswith(".png"):
            name += ".png"
        if size:
            name = os.path.join("..", size, name)
        for path in self.icon_search_path:
            filename = abs_path(path_join(path, name))
            if path_exists(filename):
                return filename

    def find_action(self, name, size="32x32"):
        return self.find(path_join("actions", name), size)


class Kde(DesktopEnvironment):

    def init(self):
        self.ini_files = {}
        self.default_icon_theme = "default.kde"
        self.kdehome = expand_user(get_env("KDEHOME", "~/.kde"))
        if self.kdehome:
            self.icon_theme_search_path.insert(
                0, os.path.join(self.kdehome, "share", "icons"))
        else:
            self.icon_theme_search_path.insert(
                0, os.path.expanduser("~/.kde4/share/icons"))
            self.icon_theme_search_path.insert(
                0, os.path.expanduser("~/.kde3/share/icons"))
            self.icon_theme_search_path.insert(
                0, os.path.expanduser("~/.kde/share/icons"))

    def kdeini(self, name, section, key, default=None):
        filename = os.path.join(
            self.kdehome, "share", "config", name)
        ini = self.ini_files.get(filename)
        if not ini:
            ini = self.kdeglobals_cfg = IniFile()
            try:
                ini.read([filename])
            except:
                pass
            self.ini_files[filename] = ini
        try:
            return ini.get(section, key) or default
        except Exception:
            return default

    def kdeglobals(self, section, key, default=None):
        return self.kdeini("kdeglobals", section, key, default)

    def current_icon_theme(self):
        return self.kdeglobals("Icons", "Theme", self.default_icon_theme)


class Gnome(DesktopEnvironment):

    def init(self):
        self.etrees = {}
        self.default_icon_theme = "gnome"

    def gconf(self, name, key, default=None):
        filename = expand_user(
            "~/.gconf/desktop/gnome/%s/%%gconf.xml" % name)
        etree = self.etrees.get(filename)
        if not etree:
            try:
                etree = ElementTree(file=open(filename))
                self.etrees[filename] = etree
                for entry in etree.findall("entry"):
                    if entry.get("name") == key:
                        return entry.find("stringvalue").text
            except Exception:
                pass
        return default

    def current_icon_theme(self):
        return self.gconf("interface", "icon_theme", self.default_icon_theme)


class Fallback(DesktopEnvironment):

    def current_icon_theme(self):
        return ""


def detect_environment():
    if get_env("KDE_FULL_SESSION", None):
        env = Kde()
    elif get_env("DESKTOP_SESSION") == "gnome" and \
            get_env("GNOME_DESKTOP_SESSION_ID"):
        env = Gnome()
    else:
        env = Fallback()
    return env


find_icon = detect_environment().find
