#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Project made to save your eyes.
Created 14.12.2015 by Abdulla Gaibullaev.
Site: http://ag-one.ru
"""

from PyQt4 import QtCore
import time


class Break(QtCore.QObject):
    """
    ============================================================
    This object represents break.
    break_time - time for break
    break_distance - time between breaks
    windows - Blackscreen instances (this is visible part of break)
    children - all other breaks with smaller break distance (to avoid break intersections)

    Usage:
        b = Break()
        b.break_time = 5*60 # <-- seconds
        b.break_distance = 55*60
        b.children = [b1, b2] # <-- b1, b2 is other Break instances
        b.windows = [w1, w2, w3] # <-- w1, w2, w3 is Blackscreen instances
        b.start()

    See ageye.py
    ============================================================
    """

    break_time = 5*60
    break_distance = 55*60
    show_status = False
    children = []
    windows = []
    timer = None
    next_timestamp = 0
    timer_stamp = 2000

    def __init__(self, parent=None):
        """
        :param parent: QtObject.
        """
        QtCore.QObject.__init__(self, parent)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.check)

    def try_show(self, force=False):
        """
        :param force: if true, it will not be try.
        else if time is over, break will be shown.
        """
        delta = time.time() - self.next_timestamp
        if delta < 0 and not force:   # <------------------------- Too early
            return
        if delta > self.timer_stamp * 10 and not force:  # <------ Error (sleep mode?)
            self.reset()
        else:   # <----------------------------------------------- Show!
            self.next_timestamp = time.time() + self.break_time
            [x.reset(self.break_time) for x in self.children]
            self.show()

    def try_hide(self):
        delta = time.time() - self.next_timestamp
        if delta < 0:   # <------------------------- Too early
            return
        if delta > self.timer_stamp * 10:    # <---- Error (sleep mode?)
            self.reset()
        else:   # <--------------------------------- Hide!
            self.next_timestamp = time.time() + self.break_distance
            self.hide()

    def check(self):
        """
        Every self.timer_stamp ms this function called by timer.
        """
        if not self.show_status:
            self.try_show()
        else:
            self.try_hide()

    def start(self, snooze=0):
        """
        :param snooze: time shift parameter
        starts breaks loop
        """
        self.timer.start(self.timer_stamp)
        self.next_timestamp = time.time() + self.break_distance + snooze

    def stop(self):
        """
        stops breaks loop
        """
        if self.timer is not None:
            self.timer.stop()

    def show(self):
        self.show_status = True
        [w.show() for w in self.windows]

    def hide(self):
        self.show_status = False
        [w.hide() for w in self.windows]

    def reset(self, snooze=0):
        self.hide()
        self.stop()
        self.start(snooze)
        [x.reset(snooze) for x in self.children]

    def snooze(self, snooze_time):
        self.next_timestamp = time.time() + snooze_time
        self.hide()
        [x.snooze(snooze_time + self.break_time) for x in self.children]


