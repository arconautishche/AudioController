import AudioRestService
from Emulator.EmulatorGUI import GPIO

print('starting service...')
AudioRestService.start_service(GPIO)
