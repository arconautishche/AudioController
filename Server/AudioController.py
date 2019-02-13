from subprocess import Popen

import yaml

BCM_INPUT_ADDRESS = range(11, 14)  # little endian: first pin is least significant bit
BCM_OUTPUTS = range(23, 26)


class Zone:
    def __init__(self, gpio, zone_id, output_id, name, output_volumes):
        self.id = zone_id
        self.__gpio = gpio
        self.__bcm = BCM_OUTPUTS[output_id]
        self.__enabled = False
        self.name = name
        self.max_volume = 133
        self.__output_volumes = output_volumes
        gpio.setup(self.__bcm, gpio.OUT, initial=gpio.HIGH)

        self.volume = 50

    @property
    def enabled(self):
        return self.__enabled

    @enabled.setter
    def enabled(self, new_val):
        if self.__enabled == new_val:
            return
        self.__enabled = new_val
        self.__gpio.output(self.__bcm, self.__gpio.LOW if self.__enabled else self.__gpio.HIGH)

    @property
    def volume(self):
        return self.__output_volumes[self.id]

    @volume.setter
    def volume(self, new_volume):
        self.__output_volumes[self.id] = max(0, min(new_volume, self.max_volume))
        self.__send_volume_signal()

    def __send_volume_signal(self):
        pass  # todo


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
        self.__gpio = gpio
        gpio.setmode(gpio.BCM)
        self.__output_volumes = [0] * len(BCM_OUTPUTS)
        self.__create_zones()
        self.__initialize_input_channels()
        self.__create_inputs()

        self.selected_input = 0

    def __create_zones(self):
        self.zones = {}
        for zone_id, name in config['zones'].items():
            self.zones[zone_id] = Zone(self.__gpio, zone_id, zone_id, name, self.__output_volumes)

    def __create_inputs(self):
        self.inputs = {}
        for input_id, input_config in enumerate(config['inputs']):
            input_class = globals()[input_config['input_class']]
            self.inputs[input_id] = input_class(self.__gpio, input_config)

    def __initialize_input_channels(self):
        for bcm in BCM_INPUT_ADDRESS:
            self.__gpio.setup(bcm, self.__gpio.OUT, initial=self.__gpio.HIGH)

    def select_input(self, input_id):
        if input_id not in self.inputs.keys():
            raise ValueError('Input id unknown')

        self.inputs[self.selected_input].disable()
        self.selected_input = input_id
        self.inputs[input_id].enable()


with open("config.yaml") as file:
    config = yaml.safe_load(file)
