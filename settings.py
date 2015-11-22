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


class AGEyeTray(QtGui.QSystemTrayIcon):
    def __init__(self, icon, parent = None):
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
           "AlickGZ9@gmail.com\n\nSpecially to save your eyes")
        self.menu.setEnabled(True)


class Settings(QtGui.QWidget):
    
    def __init__(self, app):
        super(Settings, self).__init__()
        self.ctd = 0
        self.state = 0
        self.app = app
        self.next_timer = None
        self.pause_timer = None
        self.snooze_timer = None
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
        mbs = MainBlackScreen(self.app.desktop().screenGeometry(0), self)
    
        d = QtGui.QDesktopWidget()
        bs = [BlackScreen(x, self.app.desktop().screenGeometry(x)) for x in xrange(1, d.screenCount())]
        self.screens = bs+[mbs]

    def switch(self):
        if self.ctd == 0:
            [x.show() for x in self.screens]
            self.ctd = 1
        else:
            [x.hide() for x in self.screens]
            self.ctd = 0

    def snooze_done(self):
        if self.snooze_timer is not None: self.snooze_timer.stop()
        self.pause()

    def snooze(self):
        if self.pause_timer is not None: self.pause_timer.stop()
        ms = self.settings['snooze_time']
        self.snooze_timer = QtCore.QTimer(self)
        self.snooze_timer.start(ms)
        self.switch()
        self.snooze_timer.timeout.connect(self.snooze_done)

    def stop(self):
        self.state = 0
        if self.pause_timer is not None: self.pause_timer.stop()
        if self.next_timer is not None: self.next_timer.stop()
        if self.snooze_timer is not None: self.snooze_timer.stop()
        if self.ctd == 1: self.switch()

    def start(self):
        self.state = 1
        ms = self.settings['pause_distance']
        self.next_timer = QtCore.QTimer(self)
        self.next_timer.start(ms)
        self.next_timer.timeout.connect(self.pause)

    def pause_done(self):
        if self.pause_timer is not None: self.pause_timer.stop()
        self.switch()
        ms = self.settings['pause_distance']
        self.next_timer = QtCore.QTimer(self)
        self.next_timer.start(ms)
        self.next_timer.timeout.connect(self.pause)

    def pause(self):
        if self.next_timer is not None: self.next_timer.stop()
        ms = self.settings['pause_time']
        self.pause_timer = QtCore.QTimer(self)
        self.pause_timer.start(ms)
        self.switch()
        self.pause_timer.timeout.connect(self.pause_done)


    def closeEvent(self, event):
        [x.close() for x in self.screens]
        QtGui.QWidget.closeEvent(self, event)



if __name__ == '__main__':
    from main import main
    main()