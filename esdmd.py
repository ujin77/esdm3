#!/usr/bin/python
# -*- coding: utf-8
#
#pip install python-daemon
#pip install lockfile
##pip install kafka-python

import daemon, signal
from daemon import pidfile

import argparse
import logging
import logging.handlers
import os, sys, time
import threading
# from kafka import KafkaConsumer
# from kafka.errors import KafkaError

PROG=os.path.basename(sys.argv[0]).rstrip('.py')
PROG_DESC='ESDM daemon'

class cESDM(object):
    """docstring for cESDM"""
    def __init__(self, debugging=False):
        super(cESDM, self).__init__()
        self.debugging = debugging
        self.log = logging.getLogger(PROG)
        if debugging == True:
            self.log.setLevel(logging.DEBUG)
        else:
            self.log.setLevel(logging.INFO)
        lh = logging.handlers.SysLogHandler()
        lh.setFormatter(logging.Formatter('%(filename)s[%(process)d]: %(message)s'))
        self.log.addHandler(lh)
        self._thread = None
        self._start()

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
        self.log.info("Start thread")
        while self._running:
            time.sleep(.3)
        self.log.info("Exit thread")

    def close(self):
        self._stop()

def run_program(is_debug=False, foreground=False):
    smmon = cESDM(is_debug)
    if foreground:
        print "Start", PROG
    while True:
        try:
            time.sleep(.5)
        except KeyboardInterrupt:
            smmon.close()
            if foreground:
                print "\nExit", PROG
                sys.exit()
            else:
                time.sleep(.5)

def start_daemon(pidf, logf, is_debug=False):
    ### This launches the daemon in its context
    logger = logging.getLogger(PROG+'err')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(logf)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info("start daemon")
    with daemon.DaemonContext(
        working_directory='/tmp',
        umask=0o002,
        pidfile=pidfile.TimeoutPIDLockFile(pidf),
        stderr =  fh.stream,
        stdout =  fh.stream,
        ) as context:
            run_program(is_debug)

def stop_daemon(pidf):
    if os.path.isfile(pidf):
        pid = int(open(pidf).read())
        os.kill(pid, signal.SIGTERM)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=PROG_DESC)
    parser.add_argument('-f', '--foreground', action='store_true', help='Run '+ PROG +' in foreground')
    parser.add_argument('-s', '--start', action='store_true', help="Start daemon")
    parser.add_argument('-t', '--stop', action='store_true', help="Stop daemon")
    parser.add_argument('-r', '--restart', action='store_true', help="Restart daemon")
    parser.add_argument('-d', '--debug', action='store_true', help="Start in debug mode")
    parser.add_argument('-p', '--pid-file', default='/tmp/'+ PROG +'.pid')
    parser.add_argument('-l', '--log-err', default='/tmp/'+ PROG +'.err')
    parser.add_argument('-c', '--config', default='/etc/'+ PROG +'.conf')
    args = parser.parse_args()

    if args.start:
        start_daemon(pidf=args.pid_file, logf=args.log_err, is_debug=args.debug )
    elif args.stop:
        stop_daemon(pidf=args.pid_file)
    elif args.restart:
        stop_daemon(pidf=args.pid_file)
        time.sleep(1)
        start_daemon(pidf=args.pid_file, logf=args.log_err)
    elif args.foreground:
        run_program(is_debug=args.debug, foreground=True)
    else:
        parser.print_help()
