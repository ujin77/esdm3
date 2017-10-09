#!/usr/bin/python
# -*- coding: utf-8
#
#sudo pip install minimalmodbus

import minimalmodbus
import argparse, os, sys

PROG=os.path.basename(sys.argv[0]).rstrip('.py')
PROG_DESC='Eastron SDM230 reader'

DEFAULT_CFG = {
    'portname':'/dev/ttyUSB0',
    'baudrate':9600,
    'timeout':0.5,
    'slaveaddress':1
}

class sdm(minimalmodbus.Instrument):
    """docstring for sdm"""
    def __init__(self, arg=None):
        self.__conf = arg if arg else DEFAULT_CFG 
        minimalmodbus.Instrument.__init__(self, self.get_cfg('portname'), self.get_cfg('slaveaddress'))
        if self.get_cfg('baudrate'): self.serial.baudrate = self.get_cfg('baudrate') 
        if self.get_cfg('timeout'): self.serial.timeout = self.get_cfg('timeout')
        
    def get_cfg(self, arg=None):
        if self.__conf:
            if self.__conf.get(arg):
                return self.__conf[arg] 
        return None

# instrument.serial.port          # this is the serial port name
# instrument.serial.baudrate = 19200   # Baud
# instrument.serial.bytesize = 8
# instrument.serial.parity   = serial.PARITY_NONE
# instrument.serial.stopbits = 1
# instrument.serial.timeout  = 0.05   # seconds

# instrument.address     # this is the slave address number
# instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode

regs230 = [
# Name Reg Format Symbol
('Line to neutral volts:',                   0x00,   '%6.2f', 'Volts'),
('Current:',                                 0x06,   '%6.2f', 'Amps'),
('Active power:',                            0x0c,   '%6.0f', 'Watts'),
('Apparent power:',                          0x12,   '%6.0f', 'VoltAmps'),
('Reactive power:',                          0x18,   '%6.0f', 'VAr'),
('Power factor:',                            0x1e,   '%6.3f', ''),
('Phase angle:',                             0x24,   '%6.1f', 'Degree'),
('Frequency:',                               0x46,   '%6.2f', 'Hz'),
('Import active energy:',                    0x48,   '%6.2f', 'kwh'),
('Export active energy:',                    0x4a,   '%6.2f', 'kwh'),
('Import reactive energy:',                  0x4c,   '%6.2f', 'kvarh'),
('Export reactive energy:',                  0x4e,   '%6.2f', 'kvarh'),
('Total system power demand:',               0x54,   '%6.2f', 'W'),
('Maximum total system power demand:',       0x56,   '%6.2f', 'W'),
('Current system positive power demand:',    0x58,   '%6.2f', 'W'),
('Maximum system positive power demand:',    0x5a,   '%6.2f', 'W'),
('Current system reverse power demand:',     0x5c,   '%6.2f', 'W'),
('Maximum system reverse power demand:',     0x5e,   '%6.2f', 'W'),
('Current demand:',                          0x102,  '%6.2f', 'Amps'),
('Maximum current demand:',                  0x108,  '%6.2f', 'Amps'),
('Total active energy:',                     0x156,  '%6.2f', 'kwh'),
('Total reactive energy:',                   0x158,  '%6.2f', 'kvarh'),
('Current resettable total active energy:',  0x180,  '%6.2f', 'kwh'),
('Current resettable total reactive energy:',0x182,  '%6.2f', 'kvarh'),
]

def fmt_or_dummy(regfmt, val):
    if val is None:
        return '.'*len(regfmt[2]%(0))
    return regfmt[2]%(val)


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

    i=0
    # print DEFAULT_CFG
    if args.all:
        sdm=sdm(DEFAULT_CFG)
        for reg in regs230:
            print '%2i'%i, '%42s'%reg[0], reg[2]%(sdm.read_float(reg[1], 4)), reg[3]
            i=i+1
    elif args.info:
        sdm=sdm(DEFAULT_CFG)
        reg = regs230[int(args.info)]
        print int(args.info), reg[0], reg[2]%(sdm.read_float(reg[1], 4)), reg[3]
    else:
        parser.print_help()

    # sdm=sdm()
    # instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
    # instrument.serial.baudrate = 2400
    # instrument.serial.timeout = 0.5
    # instrument.debug = True
    # print instrument.serial.baudrate
    # print instrument.read_float(0, 4)
    # for reg in regs:
    #     print reg[0], sdm.read_float(reg[1], 4)

    # values = [ sdm.read_float(reg[1], 4) for reg in regs ]
    # print values
    # outvals = list((' '.join([fmt_or_dummy(*t) for t in zip(regs, values)])).split())
    # print outvals

