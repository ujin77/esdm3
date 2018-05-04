#!/usr/bin/python
# -*- coding: utf-8
#

import daemon, signal
from daemon import pidfile
import threading
import logging
import logging.handlers
import os, sys

CONS_FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
SYSLOG_FORMAT = "%(levelname)s:%(name)s:%(message)s"
PROG=os.path.basename(sys.argv[0]).rstrip('.py')
RUN_INTERVAL = 0.2
DEV_LOG='/dev/log'

class CDaemon(object):
    """docstring for CDaemon"""
    def __init__(self, arg=None):
        super(CDaemon, self).__init__()
        self.__conf = arg
        self._thread = None
        self._start()

    def _setLog(self):
        logger = logging.getLogger()
        if not logger.handlers:
            if os.path.isfile(DEV_LOG) or os.path.islink(DEV_LOG):
                handler = logging.handlers.SysLogHandler(address=DEV_LOG)
            else:
                handler = logging.handlers.SysLogHandler()
            handler.setFormatter(logging.Formatter(SYSLOG_FORMAT))
            # logger.setLevel(loglevel)
            logger.addHandler(handler)
        if self.get_cfg('name'):
            self.log = logging.getLogger(self.get_cfg('name'))
        else:
            self.log = logging.getLogger(PROG)

    def get_cfg(self, arg=None):
        if self.__conf:
            if self.__conf.get(arg):
                return self.__conf[arg] 
        return None

    def _start(self):
        self.exit_flag = threading.Event()
        if self._thread is None:
            self._thread = threading.Thread(target=self._run)
            self._thread.daemon = True
            self._thread.start()

    def _stop(self):
        self.exit_flag.set()
        if self._thread is not None:
            if threading.current_thread() != self._thread:
                self._thread.join()
                self._thread = None

    def _run(self):
        self._setLog()
        self.log.info("Start thread")
        self.on_start()
        while not self.exit_flag.wait(timeout=RUN_INTERVAL):
            self.on_run()
        self.on_stop()
        self.log.info("Exit thread")

    def close(self):
        self.on_close()
        self._stop()

    def is_exit(self):
        self.exit_flag.is_set()

    def on_start(self):
        pass

    def on_stop(self):
        pass

    def on_run(self):
        pass

    def on_init(self):
        pass

    def on_close(self):
        pass

