#!/usr/bin/python3

import json
import urllib.request
import urllib.error
import time
import logging
import copy
from collections import deque


def get_cfg(conf, arg=None, default=None):
    return conf[arg] if conf.get(arg) else default


class TBMessage(object):

    _data = {}

    def __init__(self, json_data=None):
        if json_data:
            self._data['ts'] = int(round(time.time() * 1000))
            self._data['values'] = json_data

    def data(self):
        return json.dumps(self._data).encode('utf8')

    def get(self):
        return self.data()

    def __repr__(self):
        return str(self.data())

    def __bytes__(self):
        return self.data()


class Thingsboard(object):

    _result = ''
    _queue = None

    def __init__(self, host='127.0.0.1', port='8080', accesstoken='',
                 api='telemetry', message=None, conf=None, queue_len=1000):
        if conf:
            host = get_cfg(conf, 'host', host)
            port = get_cfg(conf, 'port', port)
            accesstoken = get_cfg(conf, 'accesstoken', accesstoken)
            self._qlen = get_cfg(conf, 'queue', queue_len)
        self._send_from_queue = False
        self._url = 'http://{}:{}/api/v1/{}/{}'.format(host, port, accesstoken, api)
        self._queue = deque()
        if message:
            self.send(message)

    def send(self, message):
        if message is None:
            raise ValueError('No message')
        self.add_queue(TBMessage(message).get())
        while len(self._queue):
            self._send()

    def _send(self):
        _msg = self._queue.popleft()
        logging.debug(self._url)
        logging.debug(_msg)
        _req = urllib.request.Request(self._url, headers={'content-type': 'application/json'}, data=_msg)
        try:
            response = urllib.request.urlopen(_req, timeout=3)
            self._result = response.getcode()
        except urllib.error.URLError as e:
            self._result = e.reason
            self.back_to_queue(_msg)
        logging.debug('Response: %s' % self._result)
        if self._result != 200:
            raise ValueError(self._result)

    def back_to_queue(self, _msg):
        logging.debug(_msg)
        if len(self._queue) < self._qlen:
            self._queue.appendleft(copy.deepcopy(_msg))

    def add_queue(self, _msg):
        logging.debug(_msg)
        if len(self._queue) < self._qlen:
            self._queue.append(copy.deepcopy(_msg))

    def __repr__(self):
        return str(self._result)

    def get_resp(self):
        return self._result
