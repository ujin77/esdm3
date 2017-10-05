#!/usr/bin/python
# -*- coding: utf-8
#
#sudo pip install python-daemon
#sudo pip install lockfile

import daemon, signal
from daemon import pidfile
import threading

CONS_FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
SYSLOG_FORMAT = "%(levelname)s:%(name)s:%(message)s"

class CDaemon(object):
    """docstring for CDaemon"""
    def __init__(self, arg=None):
        super(CDaemon, self).__init__()
        self._conf = arg
        self._thread = None
        self._start()

    def _setLog(self):
        logger = logging.getLogger()
        if not logger.handlers:
            handler = logging.handlers.SysLogHandler()
            handler.setFormatter(logging.Formatter(SYSLOG_FORMAT))
            # logger.setLevel(loglevel)
            logger.addHandler(handler)
        self.log = logging.getLogger(self._conf('name'))

    def _conf(self, arg=None):
        if self._conf:
            if self._conf[arg]:
                return self._conf[arg]
        return None

    def _start(self):
        self._running = True
        if self._thread is None:
            self._thread = threading.Thread(target=self._run)
            self._thread.daemon = True
            self._thread.start()

    def _stop(self):
        self._running = False
        if self._thread is not None:
            if threading.current_thread() != self._thread:
                self._thread.join()
                self._thread = None

    def _run(self):
        self._setLog()
        self.log.info("Start thread")
        self.on_start()
        while self._running:
            time.sleep(1)
            self.on_run()
        self.on_stop()
        self.log.info("Exit thread")

    def close(self):
        self._stop()

    def on_start(self):
        pass

    def on_stop(self):
        pass

    def on_run(self):
        pass

    def on_init(self):
        pass
