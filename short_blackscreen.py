#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Project made to save your eyes.
Created 23.11.2015 by Abdulla Gaibullaev.
Site: http://ag-one.ru
"""

import os
import random
from PyQt4 import QtGui
from main_blackscreen import MainBlackScreen
import settings


class ShortBlackScreen(MainBlackScreen):
    """
    =====================================================
    This is a implementation of short break main window.
    This window (by default) shows 5 seconds without any chance to snooze or canceling.
    =====================================================
    """

    path = settings.short_images_path

    def __init__(self, geom, settings):
        MainBlackScreen.__init__(self, geom, settings)
        MainBlackScreen.prepare(self)

    def init_images(self):
        files = os.listdir(self.path)
        self.images = filter(lambda x: x.split('.')[-1] in ['jpg', 'png'], files)

    def get_images(self):
        random.shuffle(self.images)
        return [os.path.join(self.path, x) for x in self.images], 0

    def prepare(self):
        self.next_image()

    def initUI(self):
        self.prepareUI()
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