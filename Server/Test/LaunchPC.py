from Emulator.EmulatorGUI import GPIO
from Server import StartServer


class VolumeToGui:
    def send_volumes(self, data):
        print([bin(d) for d in data])


StartServer(GPIO, volume_control=VolumeToGui)
