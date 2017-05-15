from AudioController import AudioController
from AudioRestService import AudioRestService
from Emulator.EmulatorGUI import GPIO


print('initializing...')
control = AudioController(GPIO)
service = AudioRestService()
print('starting service...')
service.start_service(control)

