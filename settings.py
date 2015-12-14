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
from break_object import Break


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
        self.init_settings()

        tray = AGEyeTray(QtGui.QIcon('icon.png'), self)
        self.make_blacks()
        tray.show()
        self.init_breaks()
        self.start()

    def init_breaks(self):
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

        self.short_break.windows = self.screens[:-2] + self.screens[-1:]
        self.main_break.windows = self.screens[:-1]

    def snooze(self, sec):
        self.main_break.snooze(sec)

    def stop(self, only_short=False):
        self.main_break.stop()
        self.short_break.stop()

    def start(self, only_short=False):
        self.main_break.start()
        self.short_break.start()

    def pause(self):
        self.main_break.try_show(force=True)


    def closeEvent(self, event):
        [x.close() for x in self.screens]
        QtGui.QWidget.closeEvent(self, event)


if __name__ == '__main__':
    from main import main
    main()