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
from blackscreen import BlackScreen

path = 'data/images'

class ClickLabel(QtGui.QLabel):
    def __init__(self, parent):
        QtGui.QLabel.__init__(self, parent)

    def mouseReleaseEvent(self, ev):
        self.emit(QtCore.SIGNAL('clicked()'))

class MainBlackScreen(BlackScreen):
    def __init__(self, geom, settings):
        self.settings = settings
        super(MainBlackScreen, self).__init__(0, geom)
        self.init_images()

    def init_images(self):
        files = os.listdir(path)
        self.images = filter(lambda x: x.split('.')[-1] in ['jpg', 'png'], files)
        self.rules = {}
        if 'rules.txt' in files:
            self.rules = {
                x.split(':')[0].strip() : map(int, x.split(':')[1].strip().split()) 
                for x in open(os.path.join(path, 'rules.txt')).read().split('\n')
            }

    def get_images(self):
        hour = datetime.datetime.now().hour
        available = [x for x in self.images if x not in self.rules or hour in self.rules[x]]
        random.shuffle(available)
        return [os.path.join(path, x) for x in available]

    def set_image(self, image):
        pm = QtGui.QPixmap(image)
        pm = pm.scaled(400, 400, Qt.KeepAspectRatio)
        self.image.setPixmap(pm)

    def prepare(self):
        self.session_images = self.get_images()
        self.current_image = 0
        self.set_image(self.session_images[0])

    def next_image(self):
        self.current_image = (self.current_image + 1) % len(self.session_images)
        self.set_image(self.session_images[self.current_image])

    def initUI(self):
        BlackScreen.initUI(self)

        snooze_btn = QtGui.QPushButton('Snooze', self)
        btn_height = 70
        snooze_btn.setFixedHeight(btn_height)
        snooze_btn.setFixedWidth(400)
        snooze_btn.setStyleSheet('border-radius: %spx; font-size: 25pt; background-color: white;' % (btn_height / 2))
        snooze_btn.clicked.connect(self.settings.snooze)

        self.image = ClickLabel(self)
        self.image.setFixedHeight(400)
        self.image.setFixedWidth(400)
        self.image.setStyleSheet('color: white; font-size: 25pt;');
        self.connect(self.image, QtCore.SIGNAL('clicked()'), self.next_image)

        grid = QtGui.QGridLayout()
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(2, 1)
        grid.setRowStretch(0, 1)
        grid.setRowStretch(3, 1)

        grid.addWidget(snooze_btn, 1, 1)
        grid.addWidget(self.image, 2, 1)

        self.setLayout(grid)


if __name__ == '__main__':
    from main import main
    main()