#!/usr/bin/python
# -*- coding: utf-8
#

import time
from threading import _Timer
from threading import Event

class RepeatTimer(_Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)
        self.finished.set()

class CTimer(object):

    events = {}
    timers = {}

    def __init__(self):
        pass

    def on_timer(self, event=None):
        if event:
            event.set()

    def start(self):
        pass

    def stop(self):
        for name, timer in self.timers.iteritems():
            timer.cancel()

    def add(self, name, interval):
        self.events[name] = Event()
        self.timers[name] = RepeatTimer(interval, self.on_timer, args=(self.events[name],))
        self.timers[name].start()

    def is_set(self,name):
        if self.events[name].is_set():
            self.events[name].clear()
            return True
        return False

def test():
    tm = CTimer()
    tm.add('test1',3)
    tm.add('test2',6)
    try:
        while True:
            if tm.is_set('test1'):
                print 'test1',time.time()
            if tm.is_set('test2'):
                print 'test2',time.time()
            time.sleep(.1)
    except KeyboardInterrupt:
        print "Exit"
    tm.stop()

if __name__ == "__main__":
    test()
