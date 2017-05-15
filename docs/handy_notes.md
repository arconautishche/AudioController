# Some Handy Notes

## Raspberry Pi

### Assembling the thing
[Pinout Scheme](http://www.raspberrypi-spy.co.uk/wp-content/uploads/2014/07/Raspberry-Pi-GPIO-Layout-Model-B-Plus.png)
- RPI-GPIO-2 - _red_ - RelayModule-VCC
- RPI-GPIO-14 - _black_ - RelayModule-GND
- RPI-GPIO-16 - _purple_ - RelayModule-in1
- RPI-GPIO-18 - _green_ - RelayModule-in2
- RPI-GPIO-20 - _blue_ - RelayModule-in3

### Credentials

- Username: pi
- Password: raspberry

*OS*: Raspbian Jessie Lite

### Service Software

#### Python Libs (pip install)
##### Client (ServiceTest)

- requests

##### Server (Service)

- web.py==0.40.dev0
