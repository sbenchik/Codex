# Codex

Codex is a text editor for programmers built with PyQt4 and QScintilla.
Latest screenshot with i3 on Linux:

![Image](https://raw.githubusercontent.com/sbenchik/QsciWriter/master/screen.png)

QsciWriter is a text editor for code made with PyQt4 and QScintilla.

Current features are:
* Syntax highlighting
* Autocompletion
* Tabs
* Embedded terminal
* Find and Replace
* Sidebar File Tree (sort of)
* Dark Mode

Features in development are:
* Snippet support
* Opening files from the file tree
* Support for more colorschemes/languages through [Pygments](http://pygments.org)
* Live preview for Markdown/ReST/HTML files
* Open files persist throughout opening/closing Codex (a la Sublime Text)

# Installation
First you'll need to install [Python 2.7.11](https://www.python.org/downloads/), [PyQt 4](https://www.riverbankcomputing.com/software/pyqt/download), and [QScintilla2](https://www.riverbankcomputing.com/software/qscintilla/download).
From there run
 
	python Codex/Writer.py

from the directory you downloaded Codex into. A more official way of installing Codex with a Makefile and whatnot is coming soon.

# Acknowledgments
Codex is inspired by/based off of a variety of projects, including [Writer by Peter Goldsborough](https://github.com/goldsborough/Writer), [Enki by Andrei Kopats](http://enki-editor.org), [Thunderpad by Alex Spataru](https://github.com/alex-spataru/Thunderpad), and [SciTE by Neil Hodgson](http://www.scintilla.org/SciTE.html).

