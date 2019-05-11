#!/usr/bin/python3

import logging
import os
import sys
import time
import json
from _timer import CTimer
from _sdm import Esdm
from _tb import Thingsboard
from _zbx import Zabbix
import config

# PROG = os.path.basename(sys.argv[0]).rstrip('.py')


class Esdm3(object):

    data_payload = {}
    _sdm = None
    _startTime = None
    _scheduler = None
    _tbdeque = None
    _tb = None
    conf = None

    def __init__(self, conf):
        self.conf = conf
        self.on_config()
        self.on_init()

    def on_init(self):
        logging.info("Start...")
        try:
            self._sdm = Esdm(self.conf.get('esdm'))
        except Exception as err:
            logging.error("Init: " + str(err))
            # self.exit_flag.set()

        self._scheduler = CTimer()
        self._startTime = time.time()
        self.data_payload['uptime'] = self.uptime()
        self._scheduler.add('main', 10)
        self._scheduler.add('demand', 300)
        self._scheduler.add('uptime', 60)
        logging.info("started")

    def on_config(self):
        if self.conf.get('zabbix'):
            logging.info('Zabbix: %s' % self.conf.get('zabbix'))
            if self.conf['zabbix'].get('log'):
                logger = logging.getLogger('pyzabbix.sender')
                logger.setLevel(logging.getLevelName(self.conf['zabbix']['log']))
        if self.conf.get('thingsboard'):
            logging.info('Thingsboard: %s' % self.conf.get('thingsboard'))
            self._tb = Thingsboard(conf=self.conf['thingsboard'])

        if self.conf.get('esdm'):
            logging.info('esdm: %s' % self.conf.get('esdm'))

    def uptime(self):
        return int(time.time() - self._startTime)

    def send_zabbix(self):
        if self.conf.get('zabbix'):
            try:
                Zabbix(conf=self.conf['zabbix'], message=self.data_payload)
            except ValueError as e:
                logging.error(e)

    def send_thingsboard(self):
        if self.conf.get('thingsboard') and self._tb is not None:
            try:
                self._tb.send(self.data_payload)
            except ValueError as e:
                logging.error(e)
            # try:
            #     while len(self._tbdeque):
            #         Thingsboard(conf=self.conf['thingsboard'], queue=self._tbdeque)
            #     Thingsboard(conf=self.conf['thingsboard'], message=self.data_payload, queue=self._tbdeque)
            # except ValueError as e:
            #     logging.error(e)

    def push_data(self):
        if len(self.data_payload):
            logging.debug(json.dumps(self.data_payload))
            self.send_zabbix()
            self.send_thingsboard()
            self.data_payload = {}

    def get_main_data(self):
        if self._scheduler.is_set('main'):
            logging.debug(self.uptime())
            if self._sdm:
                self.data_payload['uptime'] = self.uptime()
                logging.debug("Read esdm main data")
                for x in range(0, 8):
                    try:
                        data = self._sdm.get_data(x)
                        self.data_payload[data[0]] = round(data[1], 3)
                    except Exception as err:
                        logging.error("Get sdm data[" + str(x) + "]: " + str(err))
                        return

    def get_demand_data(self):
        if self._scheduler.is_set('demand'):
            logging.debug(self.uptime())
            self.data_payload['uptime'] = self.uptime()
            if self._sdm:
                logging.debug("Read esdm data")
                for x in range(8, 24):
                    try:
                        data = self._sdm.get_data(x)
                        self.data_payload[data[0]] = round(data[1], 3)
                    except Exception as err:
                        logging.error("Get sdm data[" + str(x) + "]: " + str(err))
                        return

    def get_updime(self):
        if self._scheduler.is_set('uptime'):
            logging.debug(self.uptime())
            self.data_payload['uptime'] = self.uptime()

    def run(self):
        self.get_main_data()
        self.get_demand_data()
        self.get_updime()
        self.push_data()

    def close(self):
        self._scheduler.stop()
        try:
            if self._sdm:
                self._sdm.close()
        except Exception as e:
            logging.error("sdm close: %s" % e)
        logging.info("Stopping...")


if __name__ == "__main__":

    startTime = time.time()
    loglevel = logging.getLevelName(config.CONFIG['log'])
    if loglevel == logging.DEBUG:
        logging.basicConfig(level=loglevel, format='%(levelname)s esdm %(module)s.%(funcName)s: %(message)s')
    else:
        logging.basicConfig(level=loglevel, format='%(levelname)s esdm %(funcName)s: %(message)s')
    sdm = Esdm3(config.CONFIG)

    try:
        while True:
            sdm.run()
            time.sleep(1)
    except KeyboardInterrupt:
        sdm.close()
