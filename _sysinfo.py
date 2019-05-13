#!/usr/bin/python3

import os

'''
Raspberry pi
/etc/os-release
/sys/firmware/devicetree/base/model
/proc/device-tree/model
/proc/cpuinfo
'''

RPI_MODEL = '/proc/device-tree/model'


class SysInfo(object):
    hardware = None
    uname = None

    def __init__(self):
        if os.path.isfile(RPI_MODEL):
            self.hardware = open(RPI_MODEL).readline().rstrip('\x00')
        os.cpu_count()
        self.uname = os.uname()
        # self.uname.sysname
        # self.uname.nodename
        # self.uname.release
        # self.uname.version
        # self.uname.machine



