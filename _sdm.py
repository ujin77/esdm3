#!/usr/bin/python
# -*- coding: utf-8
#

import pkgutil
import argparse, os, sys, json

def chk_module(names, desc=None):
    for name in names:
        if not pkgutil.find_loader(name):
            print 'Please install module [' + name + ']'
            print 'sudo pip install module ' + name
            sys.exit()

chk_module(['minimalmodbus'])

import minimalmodbus

PROG=os.path.basename(sys.argv[0]).rstrip('.py')
PROG_DESC='Eastron SDM230 reader'

_REG    = 0
_NAME   = 1
_DESC   = 2
_FMT    = 3
_SYMBOL = 4
_TIME   = 5

SDM230 = [
# Reg Name Description Format Symbol
(0x00, 'V',     'Line to neutral volts:',                    '6.2f', 'Volts',    5),
(0x06, 'C',     'Current:',                                  '6.2f', 'Amps',     5),
(0x0c, 'AP',    'Active power:',                             '6.0f', 'Watts',    5),
(0x12, 'APP',   'Apparent power:',                           '6.0f', 'VoltAmps', 5),
(0x18, 'RP',    'Reactive power:',                           '6.0f', 'VAr',      5),
(0x1e, 'PF',    'Power factor:',                             '6.3f', '',         5),
(0x24, 'PH',    'Phase angle:',                              '6.1f', 'Degree',   5),
(0x46, 'F',     'Frequency:',                                '6.2f', 'Hz',       5),
(0x48, 'IAE',   'Import active energy:',                     '6.2f', 'kwh',    300),
(0x4a, 'EAE',   'Export active energy:',                     '6.2f', 'kwh',    300),
(0x4c, 'IRE',   'Import reactive energy:',                   '6.2f', 'kvarh',  300),
(0x4e, 'ERE',   'Export reactive energy:',                   '6.2f', 'kvarh',  300),
(0x54, 'TSPD',  'Total system power demand:',                '6.2f', 'W',      300),
(0x56, 'MTSPD', 'Maximum total system power demand:',        '6.2f', 'W',      300),
(0x58, 'CSPPD', 'Current system positive power demand:',     '6.2f', 'W',      300),
(0x5a, 'MSPPD', 'Maximum system positive power demand:',     '6.2f', 'W',      300),
(0x5c, 'CSRPD', 'Current system reverse power demand:',      '6.2f', 'W',      300),
(0x5e, 'MSRPD', 'Maximum system reverse power demand:',      '6.2f', 'W',      300),
(0x102, 'CD',   'Current demand:',                           '6.2f', 'Amps',   300),
(0x108, 'MCD',  'Maximum current demand:',                   '6.2f', 'Amps',   300),
(0x156, 'TAE',  'Total active energy:',                      '6.2f', 'kwh',    300),
(0x158, 'TRE',  'Total reactive energy:',                    '6.2f', 'kvarh',  300),
(0x180, 'CRTAE','Current resettable total active energy:',   '6.2f', 'kwh',    300),
(0x182, 'CRTRE','Current resettable total reactive energy:', '6.2f', 'kvarh',  300)
]

DEFAULT_CFG = {
    'portname':'/dev/ttyUSB0',
    'baudrate':9600,
    'timeout':0.5,
    'slaveaddress':1,
    'dev': SDM230
}

def _dump(val):
    print json.dumps(val, indent=2)

class sdm(minimalmodbus.Instrument):
    """docstring for sdm"""
    def __init__(self, arg=None):
        self.__conf = arg if arg else DEFAULT_CFG
        try:
            minimalmodbus.Instrument.__init__(self, self.get_cfg('portname'), self.get_cfg('slaveaddress'))
        except Exception as err:
            raise err
        self.serial.baudrate = self.get_cfg('baudrate')
        self.serial.timeout = self.get_cfg('timeout')

    def get_cfg(self, arg=None):
        if self.__conf.get(arg):
            return self.__conf[arg]
        else:
            if DEFAULT_CFG.get(arg):
                return DEFAULT_CFG[arg]
        return None

    def get(self, nparam=0):
        res = 0
        try:
            res=self.read_float(SDM230[nparam][_REG], 4)
        except Exception as e:
            raise e
        return(res)

    def get_str(self, nparam=0, sfmt = False):
        reg=SDM230[nparam]
        if sfmt:
            fmt = '[{0}] {1} {2:' + reg[_FMT] + '} {3}'
        else:
            fmt = '{0:2} {1:>42} {2:' + reg[_FMT] + '} {3}'
        # print fmt
        return( fmt.format( nparam, reg[_DESC], self.get(nparam), reg[_SYMBOL]))

    def get_data(self, nparam=0):
        return( SDM230[nparam][_NAME], self.get(nparam))

    def close(self):
        try:
            self.serial.close()
        except:
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=PROG_DESC)
    parser.add_argument('-a', '--all', action='store_true', help="Display all parameters")
    parser.add_argument('-i', '--info', help="Display parameter N" )
    parser.add_argument('-p', '--port', help='Default: ' + str(DEFAULT_CFG['portname']) )
    parser.add_argument('-b', '--baudrate', help='Default: ' + str(DEFAULT_CFG['baudrate']) )
    parser.add_argument('-s', '--slaveaddress', help='Default: ' + str(DEFAULT_CFG['slaveaddress']) )
    
    args = parser.parse_args()

    if args.port:         DEFAULT_CFG['portname']=args.port
    if args.baudrate:     DEFAULT_CFG['baudrate']=int(args.baudrate)
    if args.slaveaddress: DEFAULT_CFG['slaveaddress']=int(args.slaveaddress)

    if args.all:
        sdm=sdm(DEFAULT_CFG)
        i=0
        for reg in SDM230:
            print sdm.get_str(i)
            i=i+1
    elif args.info:
        sdm=sdm(DEFAULT_CFG)
        print sdm.get_str(nparam=int(args.info), sfmt=True)
    else:
        parser.print_help()
        # _dump(DEFAULT_CFG['dev'])
        # for (x) in DEFAULT_CFG['dev']:
        #     print x[_REG]
