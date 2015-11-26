#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Text Copy project for mom.
Created 04.10.2015 by Alick
"""

import sys
from PyQt4 import QtGui, QtCore
from blackscreen import BlackScreen
from main_blackscreen import MainBlackScreen
from short_blackscreen import ShortBlackScreen


class AGEyeTray(QtGui.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtGui.QMenu(parent)
        self.parent = parent

        showAction = menu.addAction('Pause')
        showAction.triggered.connect(self.parent.pause)

        switchAction = menu.addAction('Off')
        switchAction.triggered.connect(self.switch)
        self.switchAction = switchAction

        aboutAction = menu.addAction('About')
        aboutAction.triggered.connect(self.about)

        exitAction = menu.addAction('Exit')
        exitAction.triggered.connect(self.parent.app.quit)

        self.menu = menu
        self.setContextMenu(menu)

    def switch(self):
        self.switchAction.setText(self.parent.switch_state())

    def about(self):
        self.menu.setEnabled(False)
        ans = QtGui.QMessageBox.about(None, "About", "This program written by " +
                                      "Abdulla Gaibullaev\n\nSite: ag-one.ru\nE-mail: " +
                                      "AlickGZ9@gmail.com\n\nSpecially for your eyes")
        self.menu.setEnabled(True)


class Settings(QtGui.QWidget):
    def __init__(self, app):
        super(Settings, self).__init__()
        self.ctd = [0, 0]
        self.state = 0
        self.app = app
        self.next_timer = None
        self.pause_timer = None
        self.snooze_timer = None
        self.short_pause_timer = None
        self.next_short = None
        self.init_settings()

        tray = AGEyeTray(QtGui.QIcon('icon.png'), self)
        self.make_blacks()
        tray.show()
        self.start()

    def switch_state(self):
        if self.state == 0:
            self.start()
            return 'Off'
        else:
            self.stop()
            return 'On'

    def transform_value(self, value):
        if ',' in value:
            return map(self.transform_value, value.split(','))
        if len(value.split('.')):
            try:
                parts = value.split('.')
                a, b = map(int, parts)
                return (a * 60 + b) * 1000
            except:
                pass
        return value

    def init_settings(self):
        sett = {
            x.split(':')[0].strip(): x.split(':')[1].strip()
            for x in open('settings.txt').read().split('\n')
        }
        self.settings = {k: self.transform_value(sett[k]) for k in sett}

    def make_blacks(self):
        d = QtGui.QDesktopWidget()
        bs = [BlackScreen(x, self.app.desktop().screenGeometry(x)) for x in xrange(1, d.screenCount())]

        mbs = MainBlackScreen(self.app.desktop().screenGeometry(0), self)
        sbs = ShortBlackScreen(self.app.desktop().screenGeometry(0), self)
        self.screens = bs + [mbs, sbs]

    def update_blacks(self):
        d = QtGui.QDesktopWidget()
        bs = [BlackScreen(x, self.app.desktop().screenGeometry(x)) for x in xrange(1, d.screenCount())]
        [x.close() for x in self.screens[:-2]]
        self.screens = bs + self.screens[-2:]

    def switch(self, short=False):
        indices = range(len(self.screens))
        indices = indices[:-2] + indices[-1:] if short else indices[:-1]

        if self.ctd[short] == 0:
            self.update_blacks()
            [self.screens[i].show() for i in indices]
            self.ctd[short] = 1
        else:
            [self.screens[i].hide() for i in indices]
            self.ctd[short] = 0

    def snooze_done(self):
        if self.snooze_timer is not None: self.snooze_timer.stop()
        self.pause()

    def snooze(self, msec):
        if self.pause_timer is not None: self.pause_timer.stop()
        self.snooze_timer = QtCore.QTimer(self)
        self.snooze_timer.start(int(msec))
        self.switch()
        self.snooze_timer.timeout.connect(self.snooze_done)

    def stop(self, only_short=False):
        if not only_short:
            self.state = 0
            if self.pause_timer is not None: self.pause_timer.stop()
            if self.next_timer is not None: self.next_timer.stop()
            if self.snooze_timer is not None: self.snooze_timer.stop()
            if self.ctd[0] == 1: self.switch(False)
        if self.short_pause_timer is not None: self.short_pause_timer.stop()
        if self.next_short is not None: self.next_short.stop()
        if self.ctd[1] == 1: self.switch(True)


    def start(self, only_short=False):
        if not only_short:
            self.state = 1

            ms = self.settings['pause_distance']
            self.next_timer = QtCore.QTimer(self)
            self.next_timer.start(ms)
            self.next_timer.timeout.connect(self.pause)

        sms = self.settings['short_pause_distance']
        self.next_short = QtCore.QTimer(self)
        self.next_short.start(sms)
        self.next_short.timeout.connect(self.short_pause)

    def pause_done(self):
        if self.pause_timer is not None: self.pause_timer.stop()
        self.switch()
        ms = self.settings['pause_distance']
        self.next_timer = QtCore.QTimer(self)
        self.next_timer.start(ms)
        self.start(True)
        self.next_timer.timeout.connect(self.pause)

    def short_pause_done(self):
        if self.short_pause_timer is not None: self.short_pause_timer.stop()
        self.switch(True)

    def pause(self):
        if self.next_timer is not None: self.next_timer.stop()
        ms = self.settings['pause_time']
        self.pause_timer = QtCore.QTimer(self)
        self.pause_timer.start(ms)
        self.switch()
        self.pause_timer.timeout.connect(self.pause_done)
        self.stop(True)

    def short_pause(self):
        ms = self.settings['short_pause_time']
        self.short_pause_timer = QtCore.QTimer(self)
        self.short_pause_timer.start(ms)
        self.switch(True)
        self.short_pause_timer.timeout.connect(self.short_pause_done)

    def closeEvent(self, event):
        [x.close() for x in self.screens]
        QtGui.QWidget.closeEvent(self, event)


if __name__ == '__main__':
    from main import main

    main()