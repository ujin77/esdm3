#!/usr/bin/python
# -*- coding: utf-8
#
#sudo pip install minimalmodbus

import minimalmodbus

DEFAULT_CFG = {
    'portname':'/dev/ttyUSB0',
    'baudrate':2400,
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

regs = [
# Symbol Reg# Format
( 'V:', 0x00, '%6.2f' ), # Voltage [V]
( 'Curr:', 0x06, '%6.2f' ), # Current [A]
( 'Pact:', 0x0c, '%6.0f' ), # Active Power («Wirkleistung») [W]
( 'Papp:', 0x12, '%6.0f' ), # Apparent Power («Scheinl.») [W]
( 'Prea:', 0x18, '%6.0f' ), # Reactive Power («Blindl.») [W]
( 'PF:', 0x1e, '%6.3f' ), # Power Factor [1]
( 'Phi:', 0x24, '%6.1f' ), # cos(Phi)? [1]
( 'Freq:', 0x46, '%6.2f' ), # Line Frequency [Hz]
( 'Wact:', 0x0156, '%6.2f' ), # Energy [kWh]
( 'Wrea:', 0x0158, '%6.2f' ), # Energy react [kvarh]
]

def fmt_or_dummy(regfmt, val):
    if val is None:
        return '.'*len(regfmt[2]%(0))
    return regfmt[2]%(val)


if __name__ == "__main__":
    sdm=sdm(DEFAULT_CFG)
    # instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
    # instrument.serial.baudrate = 2400
    # instrument.serial.timeout = 0.5
    # instrument.debug = True
    # print instrument.serial.baudrate
    # print instrument.read_float(0, 4)
    for reg in regs:
        print sdm.read_float(reg[1], 4)

    values = [ sdm.read_float(reg[1], 4) for reg in regs ]
    print values
    outvals = list((' '.join([fmt_or_dummy(*t) for t in zip(regs, values)])).split())
    print outvals

