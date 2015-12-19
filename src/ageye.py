#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Project made to save your eyes.
Created 14.11.2015 by Abdulla Gaibullaev.
Site: http://ag-one.ru
"""

from PyQt4 import QtGui, QtCore
from blackscreen import BlackScreen
from main_blackscreen import MainBlackScreen
from short_blackscreen import ShortBlackScreen
from break_object import Break
from tray import AGEyeTray
import settings


class AGEye(QtGui.QWidget):
    """
    ================================================
    It's main class of the program.
    Uses settings file (settings.txt)

    This is default settings content:
        pause_time: 5.00
        pause_distance: 55.00
        short_pause_time: 0.05
        short_pause_distance: 10.00
        snooze_time: 0.15, 2.00, 5.00, 60.0, 120.0

    Time format in settings is <minutes>.<seconds>
    If you need 5 hours, write 300.0
    ================================================
    """

    ctd = [0, 0]
    state = 0

    def __init__(self, app):
        """
        :param app: QApplication instance
        1) init settings
        2) make windows
        3) init reaks
        4) init tray
        5) start break loop
        6) init and start monitor count updater.
        """
        super(AGEye, self).__init__()
        self.app = app
        self.init_settings()
        self.make_blacks()
        self.init_breaks()

        tray = AGEyeTray(QtGui.QIcon(settings.tray_icon), self)
        tray.show()
        self.start()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_blacks)
        self.timer.start(1000 * 60 * 60)  # <--- every hour update monitor count.

    def init_breaks(self):
        """
        Init 2 breaks: long and short.
        """
        self.short_break = Break()
        self.short_break.break_time = self.settings['short_pause_time']
        self.short_break.break_distance = self.settings['short_pause_distance']
        self.short_break.windows = self.screens[:-2] + self.screens[-1:]

        self.main_break = Break()
        self.main_break.break_time = self.settings['pause_time']
        self.main_break.break_distance = self.settings['pause_distance']
        self.main_break.windows = self.screens[:-1]
        self.main_break.dependencies = [self.short_break]


    def switch_state(self):
        if self.state == 0:
            self.start()
            return 'Off'
        else:
            self.stop()
            return 'On'

    def transform_value(self, value):
        """
        :param value: time string (for example '5.00' or '0.25, 1.00, 5.00, 20.00')
        :return: seconds as integer value or list of ints
        """
        if ',' in value:
            return map(self.transform_value, value.split(','))
        if len(value.split('.')):
            try:
                parts = value.split('.')
                a, b = map(int, parts)
                return (a * 60 + b)
            except:
                pass
        return value

    def init_settings(self):
        sett = {
            x.split(':')[0].strip(): x.split(':')[1].strip()
            for x in open(settings.settings_file).read().split('\n')
        }
        self.settings = {k: self.transform_value(sett[k]) for k in sett}

    def make_blacks(self):
        """
        Creates all windows: main-break window, short-break window and blackscreens for other monitors.
        """
        d = QtGui.QDesktopWidget()
        bs = [BlackScreen(x, self.app.desktop().screenGeometry(x)) for x in xrange(1, d.screenCount())]

        mbs = MainBlackScreen(self.app.desktop().screenGeometry(0), self)
        sbs = ShortBlackScreen(self.app.desktop().screenGeometry(0), self)
        self.screens = bs + [mbs, sbs]

    def update_blacks(self):
        """
        Every hour update monitor count.
        """
        d = QtGui.QDesktopWidget()
        bs = [BlackScreen(x, self.app.desktop().screenGeometry(x)) for x in xrange(1, d.screenCount())]
        [x.close() for x in self.screens[:-2]]
        self.screens = bs + self.screens[-2:]

        self.short_break.windows = self.screens[:-2] + self.screens[-1:]
        self.main_break.windows = self.screens[:-1]

    def snooze(self, sec):
        self.main_break.snooze(sec)

    def stop(self):
        self.main_break.stop()
        self.short_break.stop()

    def start(self):
        self.main_break.start()
        self.short_break.start()

    def pause(self):
        self.main_break.try_show(force=True)

    def closeEvent(self, event):
        [x.close() for x in self.screens]
        QtGui.QWidget.closeEvent(self, event)

