#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Project made to save your eyes.
Created 14.11.2015 by Abdulla Gaibullaev.
Site: http://ag-one.ru
"""

from PyQt4 import QtGui


class AGEyeTray(QtGui.QSystemTrayIcon):
    """
    Tray icon class.
    Any eye saving app must have tray icon to have easy control way.

    """

    def __init__(self, icon, parent):
        """
        Parent must be AGEye instance! Not None!
        """
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
        """
        Don't touch this, please. It's only way to save my name.
        """
        self.menu.setEnabled(False)
        QtGui.QMessageBox.about(
            None, "About",
            "This program written by Abdulla Gaibullaev\n\n" +
            "Site: ag-one.ru\nE-mail: AlickGZ9@gmail.com\n\nSpecially for your eyes"
        )
        self.menu.setEnabled(True)