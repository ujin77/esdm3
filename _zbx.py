#!/usr/bin/python3

import logging
from pyzabbix import ZabbixMetric, ZabbixSender


def get_cfg(conf, arg=None, default=None):
    return conf[arg] if conf.get(arg) else default


class Zabbix(object):

    def __init__(self, host='127.0.0.1', port='10051', name='TEST', message=None, conf=None):

        if conf:
            host = get_cfg(conf, 'host', host)
            port = get_cfg(conf, 'port', port)
            name = get_cfg(conf, 'name', name)
        logging.debug('%s:%s %s' % (host, port, name))

        zbx = ZabbixSender(zabbix_server=host,
                           zabbix_port=int(port))
        metrics = []
        if message:
            for (key, val) in message.items():
                metrics.append(ZabbixMetric(name, key, val))
            try:
                zbx.send(metrics)
                # if zbx._failed != 0:
                #     print "Send to zabbix error", z_host, z_key, z_val
                #     logging.error("Send to zabbix error")
            except Exception as err:
                logging.error('Publish zabbix: %s' % (str(err)))
        else:
            raise ValueError('No message')
