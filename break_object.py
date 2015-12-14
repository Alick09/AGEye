__author__ = 'Alick'
import time
from PyQt4 import QtCore

timer_stamp = 2000

class Break(QtCore.QObject):
    """
    Usage:
        b = Break()
        b.break_time = 5*60 # <-- seconds
        b.break_distance = 55*60
        b.dependencies = [b1, b2] # <-- b1, b2 is other Break instances
        b.windows = [w1, w2, w3] # <-- w1, w2, w3 is Blackscreen instances
        b.start()
    """
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
        self.break_time = 5*60
        self.break_distance = 55*60
        self.show_status = False
        self.dependencies = []
        self.windows = []
        self.timer = None
        self.next_timestamp = 0

    def try_show(self, force=False):
        delta = time.time() - self.next_timestamp
        if delta < 0 and not force:   # <------------------------- Too early
            return
        if delta > timer_stamp * 10 and not force:  # <----------- Error (sleep mode?)
            self.reset()
        else:   # <----------------------------------------------- Show!
            self.next_timestamp = time.time() + self.break_time
            [x.reset(self.break_time) for x in self.dependencies]
            self.show()

    def try_hide(self):
        delta = time.time() - self.next_timestamp
        if delta < 0:   # <------------------------- Too early
            return
        if delta > timer_stamp * 10:    # <--------- Error (sleep mode?)
            self.reset()
        else:   # <--------------------------------- Hide!
            self.next_timestamp = time.time() + self.break_distance
            self.hide()

    def check(self):
        if not self.show_status:
            self.try_show()
        else:
            self.try_hide()

    def start(self, snooze=0):
        self.timer = QtCore.QTimer(self)
        self.timer.start(timer_stamp)
        self.timer.timeout.connect(self.check)
        self.next_timestamp = time.time() + self.break_distance

    def stop(self):
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
        [x.reset(snooze) for x in self.dependencies]

    def snooze(self, snooze_time):
        self.next_timestamp = time.time() + snooze_time
        self.hide()
        [x.snooze(snooze_time) for x in self.dependencies]


