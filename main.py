#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Text Copy project for mom.
Created 04.10.2015 by Alick
"""

import sys
from PyQt4 import QtGui
from settings import Settings


def main():
    app = QtGui.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    s = Settings(app)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

#TODO: ESC-exit on short-break
#TODO: Complex system with breaks. Simplify code understanding.
#TODO: Long break warn (30 sec)
#TODO: Snooze in tray
#TODO: Detect activity