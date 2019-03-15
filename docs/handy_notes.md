# Hardware

[Pinout Scheme](http://www.raspberrypi-spy.co.uk/wp-content/uploads/2014/07/Raspberry-Pi-GPIO-Layout-Model-B-Plus.png)
- RPI-GPIO-2 - _red_ - RelayModule-VCC
- RPI-GPIO-16 - _purple_ - RelayModule-in1
- RPI-GPIO-18 - _green_ - RelayModule-in2
- RPI-GPIO-20 - _black_ - RelayModule-GND
- RPI-GPIO-22 - _blue_ - RelayModule-in3

## Components
- Stereo audio volume control: [PGA2311](http://www.ti.com/lit/ds/symlink/pga2311.pdf)

![image](https://hackster.imgix.net/uploads/attachments/218603/6sQiFTKXhZptFiGnPlsc.png "schema")

# RaspberryPi
## Connecting

Use *PuTTY*, ssh to 192.168.1.43

- Username: pi
- Password: raspberry

## Configuration
*OS*: Raspbian Jessie Lite

## AudioController Service Software

### Python Libs (pip install)
- Client (ServiceTest)
-- requests
- Server (Service)
-- web.py==0.40.dev0

### Start service
cd /opt/audio/AudioController/
python AudioServiceRPi.py

### Configure autostart
from: http://www.instructables.com/id/Raspberry-Pi-Launch-Python-script-on-startup/

## Additional Software
### raspotify
https://github.com/dtcooper/raspotify

### mpg123 
installation: `sudo apt-get install mpg123`

play stream: `mpg123 "http://icecast.vrtcdn.be/radio1-high.mp3"`



## Additional configuration
### Issue with noice on jack out

solution: add following line in /boot/config.txt:
audio_pwm_mode=2

