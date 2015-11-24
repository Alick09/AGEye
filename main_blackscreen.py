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

    def short_name(self, msec):
        seconds = msec/1000
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return '{hours}{minutes}{seconds}'.format(
            hours = '%dh' % hours if hours else '',
            minutes = '%dm' % minutes if minutes else '',
            seconds = '%ds' % seconds if seconds or msec < 1000 else ''
        )

    def get_style_by_time(self, msec):
        r, g, b = [128] * 3
        feel_value = (msec/(5 * 60 * 60 * 1000.)) ** 0.5
        if feel_value > 1.0:
            b = 255
        else:
            shift = int(feel_value * 255)
            if shift < 128:
                g = 255 - shift
            else:
                r = shift

        return 'background-color: #%02X%02X%02X;' % (r, g, b)

    def initUI(self):
        BlackScreen.initUI(self)
        self.mapper = QtCore.QSignalMapper()

        btn_size = 70
        snooze_btns = QtGui.QHBoxLayout()
        snooze_btns.setObjectName("SnoozeButtons")
        ms = self.settings.settings['snooze_time']
        if not isinstance(ms, list):
            ms = [ms]
        for i in ms:
            btn = QtGui.QPushButton(self.short_name(i), self)
            btn.setFixedHeight(btn_size)
            btn.setFixedWidth(btn_size)
            btn.setStyleSheet('border-radius: %spx; font-size: 25pt; %s' % (btn_size / 2, self.get_style_by_time(i)))
            btn.clicked.connect(self.mapper.map)
            self.mapper.setMapping(btn, i)
            snooze_btns.addWidget(btn)

        self.mapper.mapped.connect(self.settings.snooze)

        self.image = ClickLabel(self)
        self.image.setFixedHeight(400)
        self.image.setFixedWidth(400)
        self.image.setStyleSheet('color: white; font-size: 25pt;')
        self.connect(self.image, QtCore.SIGNAL('clicked()'), self.next_image)

        grid = QtGui.QGridLayout()
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(2, 1)
        grid.setRowStretch(0, 1)
        grid.setRowStretch(3, 1)

        grid.addLayout(snooze_btns, 1, 1)
        grid.addWidget(self.image, 2, 1)

        self.setLayout(grid)


if __name__ == '__main__':
    from main import main
    main()