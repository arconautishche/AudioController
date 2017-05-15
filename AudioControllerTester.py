import AudioController
import time
from Emulator.EmulatorGUI import GPIO

ac = AudioController.AudioController(GPIO)
ac.zones[1].enable()
time.sleep(1)
ac.zones[1].disable()