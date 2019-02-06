from AudioController import AudioController
from AudioRestService import AudioRestService
import RPi.GPIO as GPIO

print('initializing...')
control = AudioController(GPIO)
service = AudioRestService()
print('starting service...')
service.start_service(control)