from subprocess import Popen

BCM_EETKAMER = 23
BCM_BADKAMER = 24
BCM_TERRAS = 25
BCM_INPUT_SELECTOR = [11, 13]  # little endian: first pin is least significant bit
INPUT_ADDRESS_NONE = 0
INPUT_ADDRESS_RPI = 1
INPUT_ADDRESS_BLUETOOTH = 2


class Zone:
    def __init__(self, gpio, id, bcm, name):
        self.id = id
        self.__gpio = gpio
        self.__bcm = bcm
        self.on = False
        self.name = name
        gpio.setup(bcm, gpio.OUT, initial=gpio.HIGH)

    def set_enabled(self, enabled):
        if self.on == enabled:
            return
        self.on = enabled
        self.__gpio.output(self.__bcm, self.__gpio.LOW if self.on else self.__gpio.HIGH)


class Input:
    def __init__(self, name, gpio, address):
        self.name = name
        self.__gpio = gpio
        self.address = address

    def enable(self):
        self.set_input()

    def set_input(self):
        for i in [0, len(BCM_INPUT_SELECTOR) - 1]:
            pinTrue = bool(self.address >> i & 1)
            pinBcm = BCM_INPUT_SELECTOR[i]
            self.__gpio.output(pinBcm, self.__gpio.LOW if pinTrue else self.__gpio.HIGH)

    def disable(self):
        pass


class SpotifyInput(Input):
    def __init__(self, name, gpio):
        Input.__init__(self, name, gpio, INPUT_ADDRESS_RPI)

    def disable(self):
        pass  # todo Stop Spotify


class StreamInput(Input):
    def __init__(self, name, gpio, url):
        Input.__init__(self, name, gpio, INPUT_ADDRESS_RPI)
        self.url = url
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
        self.__create_zones()
        self.__initialize_input_channels()
        self.__create_inputs()
        self.selected_input = 0

    def __create_zones(self):
        self.zones = {}
        self.__create_zone(1, BCM_EETKAMER, 'Eetkamer')
        self.__create_zone(2, BCM_BADKAMER, 'Badkamer')
        self.__create_zone(3, BCM_TERRAS, 'Terras')

    def __create_zone(self, id, bcm, name):
        self.zones[id] = Zone(self.__gpio, id, bcm, name)

    def __create_inputs(self):
        self.inputs = {k: v for k, v in enumerate([
            Input("None", self.__gpio, INPUT_ADDRESS_NONE),
            SpotifyInput("Spotify", self.__gpio),
            StreamInput("StuBru", self.__gpio, 'http://icecast.vrtcdn.be/stubru-high.mp3'),
            StreamInput("Radio 1", self.__gpio, 'http://icecast.vrtcdn.be/radio1-high.mp3'),
            StreamInput("Klara", self.__gpio, 'http://icecast.vrtcdn.be/klara-high.mp3'),
            Input("Bluetooth", self.__gpio, INPUT_ADDRESS_BLUETOOTH)
        ])}

    def __initialize_input_channels(self):
        for bcm in BCM_INPUT_SELECTOR:
            self.__gpio.setup(bcm, self.__gpio.OUT, initial=self.__gpio.HIGH)

    def select_input(self, input_id):
        if input_id not in self.inputs.keys():
            raise ValueError('Input id unknown')

        self.inputs[self.selected_input].disable()
        self.selected_input = input_id
        self.inputs[input_id].enable()
