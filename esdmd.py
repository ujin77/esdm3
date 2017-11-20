#!/usr/bin/python
# -*- coding: utf-8
#
#sudo pip install py-zabbix
#sudo pip install python-daemon
#sudo pip install lockfile
##sudo pip install kafka-python

import daemon, signal
from daemon import pidfile

import argparse
import logging
import logging.handlers
import os, sys, time, json
import threading

from _daemon import CDaemon
from _sdm import sdm
import ConfigParser

# from kafka import KafkaConsumer
# from kafka.errors import KafkaError
from pyzabbix import ZabbixMetric, ZabbixSender
import paho.mqtt.publish as mqtt_publish



PROG=os.path.basename(sys.argv[0]).rstrip('.py')
PROG_DESC='ESDM daemon'

CONS_FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
SYSLOG_FORMAT = "%(levelname)s:%(name)s:%(message)s"        

DEFAULT_CONFIG={
    'name':PROG
}

DEMAND_TIME = 300

def namedtuple_asdict(t):
    return({str(type(t).__name__) : dict(t._asdict())})

class ESDM(CDaemon):
    """docstring for ESDM"""
    
    zabbix = None
    thingsboard = None
    data_payload = {}

    def on_start(self):
        self._time = time.time()
        self._sdm = sdm()
        self._time=time.time()-DEMAND_TIME
        if self.get_cfg('zabbix'):
            zb = self.get_cfg('zabbix')
            self.zabbix = zb.get('host')
            self.zabbix_name = zb.get('name') if zb.get('name') else 'SDM230'
            self.log.info('send messages to zabbix: ' + self.zabbix)
        if self.get_cfg('thingsboard'):
            tb = self.get_cfg('thingsboard')
            self.thingsboard = tb.get('host')
            self.thingsboard_telemetry = tb.get('telemetry') if tb.get('telemetry') else 'v1/devices/me/telemetry'
            self.thingsboard_attributes = tb.get('attributes') if tb.get('attributes') else 'v1/devices/me/attributes'
            self.thingsboard_accesstoken = tb.get('accesstoken') if tb.get('accesstoken') else ''
            self.log.info('send messages to thingsboard: ' + self.thingsboard)

    def on_run(self):
        for x in xrange(0,8):
            data = None
            if self.is_exit():
                return
            try:
                data = self._sdm.get_data(x)
                self.data_payload[data[0]]=round(data[1],3)
            except Exception as err:
                self.log.error("Get sdm data[" + str(x) + "]: " + str(err))
                return
        if time.time() - self._time > DEMAND_TIME:
            self._time=time.time()
            for x in xrange(8,24):
                data = None
                if self.is_exit():
                    return
                try:
                    data = self._sdm.get_data(x)
                    self.data_payload[data[0]]=round(data[1],3)
                except Exception as err:
                    self.log.error("Get sdm data[" + str(x) + "]: " + str(err))
                    return
        self.push_data()
    
    def on_stop(self):
        self._sdm.close()

    def send_zabbix(self):
        # self.log.debug("Send to zabbix " + z_key + "="+ z_val)
        metrics = []
        for (key, val) in self.data_payload.items():
            metrics.append(ZabbixMetric(self.zabbix_name, key, val))
        try:
            result = ZabbixSender(self.zabbix).send(metrics)
            # if result._failed != 0:
            #     print "Send to zabbix error", z_host, z_key, z_val
                # self.log.error("Send to zabbix error")
        except Exception as err:
            self.log.error('Publish zabbix: ' + str(err))

    def send_thingsboard(self):
        try:
            mqtt_publish.single(
                self.thingsboard_telemetry,
                payload=json.dumps(self.data_payload),
                hostname=self.thingsboard,
                auth={'username':self.thingsboard_accesstoken, 'password':""}
            )
        except Exception as err:
            self.log.error('Publish thingsboard: ' + str(err))


    def push_data(self):
        # print json.dumps(self.data_payload)
        if self.thingsboard:
            self.send_thingsboard()
        if self.zabbix:
            self.send_zabbix()
        self.data_payload = {}

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
        print "Not running"

def load_config(fname):
    if os.path.isfile(fname):
        config = ConfigParser.ConfigParser(allow_no_value=True)
        try:
            config.readfp(open(fname))
            for section in config.sections():
                for (name, value) in config.items(section):
                    if not DEFAULT_CONFIG.get(section): DEFAULT_CONFIG[section]={} 
                    DEFAULT_CONFIG[section][name] = value.strip("'\"")        
        except ConfigParser.MissingSectionHeaderError as e:
            print e
        except Exception as e:
            print e
        
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
    parser.add_argument('-v', '--verbose', action='store_true', help="Verbose output")

    args = parser.parse_args()

    if args.debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    if args.foreground:
        logging.basicConfig(level=loglevel, format=CONS_FORMAT)

    logger = logging.getLogger()
    logger.setLevel(loglevel)

    if args.config: load_config(args.config)

    if args.verbose: print 'CONFIG:', json.dumps(DEFAULT_CONFIG, indent=2)

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

