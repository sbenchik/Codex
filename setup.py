#!/usr/bin/env python
import sys, pkgutil, platform
from distutils.core import setup

def checkDeps():
""" Check if necessary dependencies are installed"""
    ok = True
    try:
        import PyQt4
    except ImportError as e:
        print("Failed to import Qt Python bindings." + "\n" +
        "See https://www.riverbankcomputing.com/software/pyqt/download")
        print e
        ok = False
    try:
        import PyQt4.Qsci
    except ImportError as e:
        print("Failed to import QScintilla Python bindings" + "\n" +
              "See https://www.riverbankcomputing.com/software/qscintilla/download")
        print e
        ok = False

    return ok

classifiers = ['Development Status :: 5 - Production/Stable',
'Environment :: X11 Applications :: Qt',
'Intended Audience :: Developers',
'Natural Language :: English',
'Operating System :: OS Independent',
'Programming Language :: Python',
'Topic :: Software Development',
'Topic :: Text Editors :: Integrated Development Environments (IDE)'
]

if sys.platform.startswith("linux") and not "sdist" in sys.argv or "upload" \
    in sys.argv:
    data_files = [
         ('/usr/share/pixmaps/', ['icons/48x48/codex.png']),
         ('/usr/share/icons/hicolor/32x32/apps', ['icons/32x32/codex.png']),
         ('/usr/share/icons/hicolor/48x48/apps', ['icons/48x48/codex.png']),
         ('/usr/share/icons/hicolor/scalable/apps', ['icons/codex.svg']),
         ('/usr/share/icons/hicolor/256x256/apps', ['icons/256x256/codex.png']),
        ]
else:
    data_files = []

packages = ["ext"]

script = "bin/codex"

if __name__ == '__main__':
    if "install" in sys.argv:
        if "--force" not in sys.argv and "--help" not in sys.argv:
            if not checkDeps():
                sys.exit()
    setup(name="Codex",
    version="1.1",
    description="Advanced text editor for code",
    author="Steve Benchik",
    author_email="stevebenchik@gmail.com",
    url= "https://github.com/sbenchik/codex",
    download_url="https://github.com/sbenchik/codex/releases",
    packages=packages,
    package_data=package_data,
    scripts=script,
    data_files=data_files,
    classifiers=classifiers,
    )
