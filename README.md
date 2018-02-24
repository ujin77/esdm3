# esdmd

## Getting Started

### Prerequisites

### Installing

### SDM230 attributes

register
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
