import RPi.GPIO as GPIO

import RestService

print('starting service...')
RestService.start_service(GPIO)
