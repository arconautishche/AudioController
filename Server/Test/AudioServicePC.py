import RestService
from AudioController import AudioController
from Emulator.EmulatorGUI import GPIO

class VolumeToGui:
    def send_volumes(self, data):
        print([bin(d) for d in data])


print('starting service...')
ac = AudioController(GPIO, volume_control=VolumeToGui)
RestService.start_service(ac)
