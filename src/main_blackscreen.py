#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Project made to save your eyes.
Created 14.11.2015 by Abdulla Gaibullaev.
Site: http://ag-one.ru
"""

import os
import re
import random
import datetime
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from blackscreen import BlackScreen
import settings


class ClickLabel(QtGui.QLabel):
    """
    ==========================
    Clickable label.
    ==========================
    """
    def __init__(self, parent):
        QtGui.QLabel.__init__(self, parent)

    def mouseReleaseEvent(self, ev):
        self.emit(QtCore.SIGNAL('clicked()'))


class MainBlackScreen(BlackScreen):
    """
    ============================================================
    This class implements long break main window.
    Windows with image and several buttons (snooze buttons).

    This class uses images and text file with time rules.
    Images in data/images and here is text file time-rules.txt

    time-rules.txt contain rules for showing particular images in particular hours.
    Example:
        .* : 8 - 23
        bed : 0 - 6

    (Regular expressions are allowed.)
    Single rule have such syntax:
        <regular expression for image name> : <hours>

        <hours> can be:
            0 - 6
            0 - 3, 5 - 12
            1, 3, 5, 7, 9
            3 - 23

        but couldn't be:
            1 - 24 (0, not 24, use 0 - 23)
            22 - 0 (in x - y rule x must be less than y, use 22, 23, 0)
            <empty>

    If image will not be in rules, 0 - 23 rule will be applied by default.

    Usage - see blackscreen.py
    ==============================================================
    """

    current_image = 0
    path = settings.images_path
    zero_image = settings.zero_image_name

    def __init__(self, geom, settings):
        """
        :param geom: param from blackscreen.py
        :param settings: AGEye instance
        """
        self.settings = settings
        BlackScreen.__init__(self, 0, geom)
        self.init_images()

    def get_hours(self, s):
        """
        :param s: string of time rules (0 - 6, 14 - 16, 22, 23)
        :return: list of hours [0, 1, 2, 3, 4, 5, 6, 14, 15, 16, 22, 23]
        """
        result = []
        ranges = re.findall(r'(\d+)\s*-\s*(\d+)', s)
        result += sum([range(int(a), int(b) + 1) for a, b in ranges], [])
        s = re.sub(r'(\d+)\s*-\s*(\d+)', '', s)
        result += map(int, re.findall(r'\d+', s))
        return sorted(result)

    def normalize_rules(self):
        """
        finds rules for each images (uses last matching rule)
        """
        old_rules = self.rules
        self.rules = {}
        for i in self.images:
            hours = range(24)
            for regex, h in old_rules:
                if re.match(regex, i) is not None:
                    hours = h
            self.rules[i] = hours


    def init_images(self):
        """
        reads all images and inits normalized rules
        """
        files = os.listdir(self.path)
        self.images = filter(lambda x: x.split('.')[-1] in settings.image_formats, files)
        self.rules = []
        if os.path.isfile(settings.time_rules_path):
            self.rules = [
                (x.split(':')[0].strip() , self.get_hours(x.split(':')[1].strip()))
                for x in open(settings.time_rules_path).read().split('\n')
            ]
        self.normalize_rules()

    def get_images(self):
        """
        :return: all available images (by time rule) for now.
        """
        hour = datetime.datetime.now().hour
        available = [x for x in self.images if x not in self.rules or hour in self.rules[x]]
        random.shuffle(available)
        index = 0
        if self.zero_image in available:
            index = available.index(self.zero_image)
        return [os.path.join(self.path, x) for x in available], index

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

    @staticmethod
    def short_name(seconds):
        sec = seconds
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return '{hours}{minutes}{seconds}'.format(
            hours='%dh' % hours if hours else '',
            minutes='%dm' % minutes if minutes else '',
            seconds='%ds' % seconds if seconds or sec < 60 else ''
        )

    def get_style_by_time(self, sec):
        """
        :param sec: seconds
        :return: css background rule

        Long snooze is less preferred. Therefore appropriate buttons will be RED!
        Short snooze will be green.
        """
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
