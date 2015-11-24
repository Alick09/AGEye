#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Text Copy project for mom.
Created 04.10.2015 by Alick
"""

import os
import random
import datetime
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from main_blackscreen import MainBlackScreen

path = 'data/images'

class ShortBlackScreen(MainBlackScreen):
    def __init__(self, geom, settings):
        MainBlackScreen.__init__(self, geom, settings)
        MainBlackScreen.prepare(self)

    def init_images(self):
        files = os.listdir(os.path.join(path, 'short-breaks'))
        self.images = filter(lambda x: x.split('.')[-1] in ['jpg', 'png'], files)

    def get_images(self):
        random.shuffle(self.images)
        return [os.path.join(path, 'short-breaks', x) for x in self.images]

    def prepare(self):
        self.next_image()

    def initUI(self):
        self.image = QtGui.QLabel(self)
        self.image.setFixedHeight(400)
        self.image.setFixedWidth(400)
        self.image.setStyleSheet('color: white; font-size: 25pt;')

        grid = QtGui.QGridLayout()
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(2, 1)
        grid.setRowStretch(0, 1)
        grid.setRowStretch(2, 1)

        grid.addWidget(self.image, 1, 1)

        self.setLayout(grid)


if __name__ == '__main__':
    from main import main
    main()