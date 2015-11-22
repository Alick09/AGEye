#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Text Copy project for mom.
Created 04.10.2015 by Alick
"""

import sys
from PyQt4 import QtGui


class BlackScreen(QtGui.QWidget):
    
    def __init__(self, id, geom):
        super(BlackScreen, self).__init__()
        self.geom = geom
        self.id = id
        self.initUI()
    
    def prepare(self):
        pass

    def show(self):
        geom = self.geom
        self.move(geom.left(), geom.top())
        self.prepare()
        self.showFullScreen()
        #self.setGeometry(30, 30, 500, 500)
        #QtGui.QWidget.show(self)

    def initUI(self):
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        
        self.setToolTip('This program designed specially to save your eyes. Written by <b>AG</b> in 2015.')
        self.setStyleSheet('background-color: black;')
        
        self.setWindowTitle('Black Screen #%s' % self.id)
     