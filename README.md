# Codex

**If you want a stable product, use the releases. Master is almost always broken.**

Codex is a text editor for programmers built with PyQt4 and QScintilla.
Latest screenshot with i3 on Linux:

![Image](https://raw.githubusercontent.com/sbenchik/QsciWriter/master/screen.png)

Current features are:
* Syntax highlighting
* Autocompletion
* Tabs
* Embedded terminal
* Find and Replace
* File Tree Sidebar

Features in development are:
* More advanced autocomplete 
* Opening files from the file tree
* Live preview for Markdown/ReST/HTML files

# Installation
## From Executable- Recommended
Simply download the latest release from "Releases", unzip the file, and run the executable (either "Codex" or "Writer")
## From Source- Advanced
First you'll need to install [Python 2.7.11](https://www.python.org/downloads/), [PyQt 4.11.4](https://www.riverbankcomputing.com/software/pyqt/download), and [QScintilla2](https://www.riverbankcomputing.com/software/qscintilla/download).
From there run

	python Codex/Codex

from the directory you downloaded Codex into. Currently Codex has only been tested on Linux (Ubuntu 16.04), but it should work fine on OS X providedan X server like XQuartz is running. 

# Acknowledgments
The icon is made by [Logo_Jim](http://electriceyecreations.tumblr.com) from Reddit.

Codex is inspired by/based off of a variety of projects, including [Writer by Peter Goldsborough](https://github.com/goldsborough/Writer), [Enki by Andrei Kopats](http://enki-editor.org), [Thunderpad by Alex Spataru](https://github.com/alex-spataru/Thunderpad), and [SciTE by Neil Hodgson](http://www.scintilla.org/SciTE.html).

