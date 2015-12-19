#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Project made to save your eyes.
Created 14.11.2015 by Abdulla Gaibullaev.
Site: http://ag-one.ru
"""

import sys
from PyQt4 import QtGui
from ageye import AGEye


def main():
    app = QtGui.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    AGEye(app)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

# TODOs:
#TODO: Long break warn (30 sec)
#TODO: Snooze in tray
#TODO: Detect activity