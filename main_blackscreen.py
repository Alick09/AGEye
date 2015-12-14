#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Text Copy project for mom.
Created 04.10.2015 by Alick
"""

import os
import re
import random
import datetime
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from blackscreen import BlackScreen

path = 'data/images'
zero_image = 'zero.jpg'

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

    def get_hours(self, s):
        result = []
        ranges = re.findall(r'(\d+)\s*-\s*(\d+)', s)
        result += sum([range(int(a), int(b) + 1) for a, b in ranges], [])
        s = re.sub(r'(\d+)\s*-\s*(\d+)', '', s)
        result += map(int, re.findall(r'\d+', s))
        return sorted(result)

    def normalize_rules(self):
        old_rules = self.rules
        self.rules = {}
        for i in self.images:
            hours = range(24)
            for regex, h in old_rules:
                if re.match(regex, i) is not None:
                    hours = h
            self.rules[i] = hours


    def init_images(self):
        files = os.listdir(path)
        self.images = filter(lambda x: x.split('.')[-1] in ['jpg', 'png'], files)
        self.rules = []
        if 'time-rules.txt' in files:
            self.rules = [
                (x.split(':')[0].strip() , self.get_hours(x.split(':')[1].strip()))
                for x in open(os.path.join(path, 'time-rules.txt')).read().split('\n')
            ]
        self.normalize_rules()

    def get_images(self):
        hour = datetime.datetime.now().hour
        available = [x for x in self.images if x not in self.rules or hour in self.rules[x]]
        random.shuffle(available)
        index = 0
        if zero_image in available:
            index = available.index(zero_image)
        return [os.path.join(path, x) for x in available], index

    def set_image(self, image):
        pm = QtGui.QPixmap(image)
        pm = pm.scaled(400, 400, Qt.KeepAspectRatio)
        self.image.setPixmap(pm)

    def prepare(self):
        self.session_images, self.current_image = self.get_images()
        self.set_image(self.session_images[self.current_image])

    def next_image(self):
        self.current_image = (self.current_image + 1) % len(self.session_images)
        self.set_image(self.session_images[self.current_image])

    def short_name(self, seconds):
        sec = seconds
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return '{hours}{minutes}{seconds}'.format(
            hours = '%dh' % hours if hours else '',
            minutes = '%dm' % minutes if minutes else '',
            seconds = '%ds' % seconds if seconds or sec < 60 else ''
        )

    def get_style_by_time(self, sec):
        r, g, b = [30] * 3
        feel_value = (sec/(3.0 * 60 * 60)) ** 0.3
        if feel_value > 1.0:
            b = 255
        else:
            shift = int(feel_value * 255)
            g = 255 - shift
            r = shift

        return 'background-color: #%02X%02X%02X;' % (r, g, b)

    def prepareUI(self):
        BlackScreen.initUI(self)

    def initUI(self):
        self.prepareUI()
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