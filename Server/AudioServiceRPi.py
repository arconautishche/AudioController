import RPi.GPIO as GPIO

import AudioRestService

print('starting service...')
AudioRestService.start_service(GPIO)
