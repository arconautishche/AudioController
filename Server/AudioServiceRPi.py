import RPi.GPIO as GPIO
from AudioController import AudioController

import RestService

print('starting service...')
ac = AudioController(GPIO)
RestService.start_service(ac)
