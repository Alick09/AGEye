#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Project made to save your eyes.
Created 14.11.2015 by Abdulla Gaibullaev.
Site: http://ag-one.ru
"""

from PyQt4 import QtGui
from PyQt4.QtCore import Qt


class BlackScreen(QtGui.QWidget):
    """
    ======================================================================================
    This is a class implements fullscreen black window (with opacity).
    It's used to make other screens (with buttons and other window elements,
                                    see main_blackscreen and short_blackscreen)

    Usage:
        d = QtGui.QDesktopWidget()
        bs = [BlackScreen(x, self.app.desktop().screenGeometry(x)) for x in xrange(1, d.screenCount())]
        ...
        [x.show() for x in bs]

    (see ageye.py (make_blacks method))
    ======================================================================================
    """
    def __init__(self, _id, geom):
        super(BlackScreen, self).__init__()
        self.geom = geom
        self.id = _id
        self.initUI()
    
    def prepare(self):
        """
        In inheritances redefine this function.
        It's calls before showing window.
        """
        pass

    def show(self):
        self.move(self.geom.left(), self.geom.top())
        self.prepare()
        self.showFullScreen()

    def initUI(self):
        """
        In inheritances redefine this function to add new GUI elements or redesign window.
        """
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        self.setStyleSheet('background-color: black;')
        self.setWindowOpacity(0.9)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Black Screen #%s' % self.id)

    def closeEvent(self, QCloseEvent):
        QCloseEvent.ignore()