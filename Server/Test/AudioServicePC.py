import RestService
from Emulator.EmulatorGUI import GPIO

print('starting service...')
RestService.start_service(GPIO)
