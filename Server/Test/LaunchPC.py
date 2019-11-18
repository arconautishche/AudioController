from Emulator.EmulatorGUI import GPIO
from Server import StartServer
from logging import log, DEBUG


class VolumeToGui:
    def send_volumes(self, data):
        data_binary_formatted = [bin(d) for d in data]
        log(DEBUG, "sending to SPI: {}".format(data_binary_formatted))


StartServer(GPIO, volume_control=VolumeToGui)
