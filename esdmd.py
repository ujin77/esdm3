#!/usr/bin/python
# -*- coding: utf-8
#
#sudo pip install python-daemon
#sudo pip install lockfile
##sudo pip install kafka-python

import daemon, signal
from daemon import pidfile

import argparse
import logging
import logging.handlers
import os, sys, time
import threading
# from kafka import KafkaConsumer
# from kafka.errors import KafkaError
from _daemon import CDaemon

PROG=os.path.basename(sys.argv[0]).rstrip('.py')
PROG_DESC='ESDM daemon'

CONS_FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
SYSLOG_FORMAT = "%(levelname)s:%(name)s:%(message)s"        

DEFAULT_CONFIG={
    'name':PROG,
}

def namedtuple_asdict(t):
    return({str(type(t).__name__) : dict(t._asdict())})

class ESDM(CDaemon):
    """docstring for ESDM"""
    def on_run(self):
        print 1        

def run_program(foreground=False):
    if foreground:
        print "Start", PROG
    # esdm = cESDM(DEFAULT_CONFIG)
    esdm = ESDM(DEFAULT_CONFIG)
    try:
        while True:
            time.sleep(.5)
    except KeyboardInterrupt:
        esdm.close()
        if foreground:
            print "Exit", PROG
            sys.exit()
    except:
        esdm.close()
        time.sleep(.5)

def start_daemon(pidf, logf):
    ### This launches the daemon in its context
    fh = logging.FileHandler(logf)
    with daemon.DaemonContext(
        working_directory='/tmp',
        umask=0o002,
        pidfile=pidfile.TimeoutPIDLockFile(pidf),
        stderr =  fh.stream,
        stdout =  fh.stream,
        ) as context:
            run_program()

def stop_daemon(pidf):
    if os.path.isfile(pidf):
        pid = int(open(pidf).read())
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError as e:
            os.remove(pidf)
        except Exception as e:
            raise
        else:
            pass
        finally:
            pass
    else:
        print "dd"
        
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

    if args.debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    if args.foreground:
        logging.basicConfig(level=loglevel, format=CONS_FORMAT)

    logger = logging.getLogger()
    logger.setLevel(loglevel)

    if args.start:
        start_daemon(pidf=args.pid_file, logf=args.log_err )
    elif args.stop:
        stop_daemon(pidf=args.pid_file)
    elif args.restart:
        stop_daemon(pidf=args.pid_file)
        time.sleep(1)
        start_daemon(pidf=args.pid_file, logf=args.log_err)
    elif args.foreground:
        run_program(foreground=True)
    else:
        parser.print_help()
