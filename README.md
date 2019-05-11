##install
```
sudo apt install python-pip 
sudo pip3 install -r requirements.txt
```
rename config.py.example to config.py and edit

##startup Systemd
edit file esdm3.service, change path to esdm3.py

```
sudo cp esdm3.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable esdm3.service
```

***
###To start esdm3 service
``sudo systemctl start esdm3.service``

###To stop esdm3 service
``sudo systemctl stop esdm3.service``

###To restart esdm3 service
``sudo systemctl restart esdm3.service``

***
## SDM230 attributes

| reg |atttr|description                             | units  |
|---  |---  |---                                     |---     |
|0x00 |V    |Line to neutral volts                   |Volts   |
|0x06 |C    |Current                                 |Amps    |
|0x0c |AP   |Active power                            |Watts   |
|0x12 |APP  |Apparent power                          |VoltAmps|
|0x18 |RP   |Reactive power                          |VAr     |
|0x1e |PF   |Power factor                            |        |
|0x24 |PH   |Phase angle                             |Degree  |
|0x46 |F    |Frequency                               |Hz      |
|0x48 |IAE  |Import active energy                    |kwh     |
|0x4a |EAE  |Export active energy                    |kwh     |
|0x4c |IRE  |Import reactive energy                  |kvarh   |
|0x4e |ERE  |Export reactive energy                  |kvarh   |
|0x54 |TSPD |Total system power demand               |W       |
|0x56 |MTSPD|Maximum total system power demand       |W       |
|0x58 |CSPPD|Current system positive power demand    |W       |
|0x5a |MSPPD|Maximum system positive power demand    |W       |
|0x5c |CSRPD|Current system reverse power demand     |W       |
|0x5e |MSRPD|Maximum system reverse power demand     |W       |
|0x102|CD   |Current demand                          |Amps    |
|0x108|MCD  |Maximum current demand                  |Amps    |
|0x156|TAE  |Total active energy                     |kwh     |
|0x158|TRE  |Total reactive energy                   |kvarh   |
|0x180|CRTAE|Current resettable total active energy  |kwh     |
|0x182|CRTRE|Current resettable total reactive energy|kvarh   |
