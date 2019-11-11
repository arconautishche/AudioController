from subprocess import Popen
import spidev

import yaml

BCM_INPUT_ADDRESS = (16, 20, 21)  # little endian: first pin is least significant bit
BCM_OUTPUTS = range(23, 26)
MAX_VOLUME = 133


# Zone = namedtuple('Zone', "zone_id name bcm enabled volume")


# class VolumeControl:
#     def __init__(self):
#         self.spi = spidev.SpiDev()


# data class
class Zone:
    def __init__(self, id, name, bcm, enabled, volume):
        self.id = id
        self.name = name
        self.bcm = bcm
        self.enabled = enabled
        self.volume = volume


#
#     @property
#     def enabled(self):
#         return self.__enabled
#
#     @enabled.setter
#     def enabled(self, new_val):
#         if self.__enabled == new_val:
#             return
#         self.__enabled = new_val
#         self.__gpio.output(self.__bcm, self.__gpio.LOW if self.__enabled else self.__gpio.HIGH)
#
#     @property
#     def volume(self):
#         return self.__output_volumes[self.id]
#
#     @volume.setter
#     def volume(self, new_volume):
#         self.__output_volumes[self.id] = max(0, min(new_volume, self.max_volume))
#         self.__send_volume_signal()
#
#     def __send_volume_signal(self):
#         pass  # todo


class Input:
    def __init__(self, gpio, name, address):
        self.name = name
        self.__gpio = gpio
        self.address = address

    def enable(self):
        self.set_input()

    def set_input(self):
        for i in range(len(BCM_INPUT_ADDRESS)):
            pin_true = bool(self.address >> i & 1)
            pin_bcm = BCM_INPUT_ADDRESS[i]
            self.__gpio.output(pin_bcm, self.__gpio.LOW if pin_true else self.__gpio.HIGH)

    def disable(self):
        pass


class AuxInput(Input):
    def __init__(self, gpio, input_config):
        Input.__init__(self, gpio, input_config['name'], input_config['address'])


class SpotifyInput(Input):
    def __init__(self, gpio, input_config):
        Input.__init__(self, gpio, input_config['name'], config['input_address_rpi'])

    def disable(self):
        pass  # todo Stop Spotify


class StreamInput(Input):
    def __init__(self, gpio, input_config):
        Input.__init__(self, gpio, input_config['name'], config['input_address_rpi'])
        self.url = input_config['url']
        self.player_process = None

    def enable(self):
        self.set_input()
        self.player_process = Popen(["mpg123", self.url])

    def disable(self):
        if self.player_process and not self.player_process.poll():
            self.player_process.kill()
        self.player_process = None


class AudioController:
    def __init__(self, gpio):
        self._gpio = gpio
        gpio.setmode(gpio.BCM)
        self._create_zones()
        self._initialize_input_channels()
        self._create_inputs()

        self.selected_input = 0

    def _create_zones(self):
        self.zones = {}
        gpio = self._gpio
        for zone_id, name in config['zones'].items():
            bcm = BCM_OUTPUTS[zone_id]
            self.zones[zone_id] = Zone(zone_id, name, bcm, False, 50)
            gpio.setup(bcm, gpio.OUT, initial=gpio.HIGH)  # configure gpio, default off

    def _create_inputs(self):
        self.inputs = {}
        for input_id, input_config in enumerate(config['inputs']):
            input_class = globals()[input_config['input_class']]
            self.inputs[input_id] = input_class(self._gpio, input_config)

    def _initialize_input_channels(self):
        for bcm in BCM_INPUT_ADDRESS:
            self._gpio.setup(bcm, self._gpio.OUT, initial=self._gpio.HIGH)

    def select_input(self, input_id):
        if input_id not in self.inputs.keys():
            raise ValueError('Input id unknown')

        self.inputs[self.selected_input].disable()
        self.selected_input = input_id
        self.inputs[input_id].enable()

    def set_zone_enabled(self, zone_id, enabled):
        zone = self.zones[zone_id]
        if zone.enabled == enabled:
            return
        zone.enabled = enabled
        self._gpio.output(zone.bcm, self._gpio.LOW if enabled else self._gpio.HIGH)

    def _send_volumes(self):
        output_volumes = [0] * len(BCM_OUTPUTS)

    def set_zone_volume(self, zone_id, volume):
        zone = self.zones[zone_id]
        zone.volume = min(volume, MAX_VOLUME)
        self._send_volumes()


with open("config.yaml") as file:
    config = yaml.safe_load(file)
