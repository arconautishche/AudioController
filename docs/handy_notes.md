# Some Handy Notes

## Raspberry Pi

### Assembling the thing
[Pinout Scheme](http://www.raspberrypi-spy.co.uk/wp-content/uploads/2014/07/Raspberry-Pi-GPIO-Layout-Model-B-Plus.png)
- RPI-GPIO-2 - _red_ - RelayModule-VCC
- RPI-GPIO-16 - _purple_ - RelayModule-in1
- RPI-GPIO-18 - _green_ - RelayModule-in2
- RPI-GPIO-20 - _black_ - RelayModule-GND
- RPI-GPIO-22 - _blue_ - RelayModule-in3

### Connect to the RaspberyPi

Use *PuTTY*, ssh to 192.168.1.43

- Username: pi
- Password: raspberry

*OS*: Raspbian Jessie Lite

### Service Software

#### Python Libs (pip install)
##### Client (ServiceTest)

- requests

##### Server (Service)

- web.py==0.40.dev0

### Start service
cd /opt/audio/AudioController/
python AudioServiceRPi.py

#### Configure autostart
from: http://www.instructables.com/id/Raspberry-Pi-Launch-Python-script-on-startup/

### Install Spotify server (mopidy)
from: https://docs.mopidy.com/en/latest/installation/debian/#debian-install

wget -q -O - https://apt.mopidy.com/mopidy.gpg | sudo apt-key add -

-> mopidy not needed...
### install despotify
http://mitchfournier.com/2013/03/26/install-command-line-spotify-on-a-headless-raspberry-pi/
