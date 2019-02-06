from subprocess import Popen


class AudioController:
    INPUT_SELECTOR_BCM = [11, 13]  # little endian: first pin is least significant bit

    def __init__(self, gpio):
        self.__gpio = gpio
        gpio.setmode(gpio.BCM)
        self.__create_zones()
        self.__create_inputs()
        self.__setup_input_BCMs()
        self.selected_input = 1
        self.__stream_play_processes = []

    def __create_zones(self):
        self.zones = {}
        self.__create_zone(1, 23, 'Eetkamer')
        self.__create_zone(2, 24, 'Badkamer')
        self.__create_zone(3, 25, 'Terras')

    def __create_zone(self, id, bcm, name):
        self.zones[id] = Zone(self.__gpio, id, bcm, name)

    def __create_inputs(self):
        self.inputs = {
            1: {'name': 'Spotify',
                'type': 'software'},
            2: {'name': 'StuBru',
                'type': 'stream',
                'url': 'http://icecast.vrtcdn.be/stubru-high.mp3'},
            3: {'name': 'Radio 1',
                'type': 'stream',
                'url': 'http://icecast.vrtcdn.be/radio1-high.mp3'},
            4: {'name': 'Klara',
                'type': 'stream',
                'url': 'http://icecast.vrtcdn.be/klara-high.mp3'},
            5: {'name': 'Bluetooth',
                'type': 'aux'}
        }

    def __setup_input_BCMs(self):
        for bcm in self.INPUT_SELECTOR_BCM:
            self.__gpio.setup(bcm, self.__gpio.OUT, initial=self.__gpio.HIGH)

    def select_input(self, input_id):
        if input_id not in self.inputs.keys():
            raise ValueError('Input id unknown')

        for p in self.__stream_play_processes:
            p.kill()
            self.__stream_play_processes.remove(p)

        inp = self.inputs[input_id]

        if inp['type'] == 'stream':
            self.__play_stream(inp['url'])

        self.selected_input = input_id

    def select_aux_channel(self, address):
        for i in [0, len(self.INPUT_SELECTOR_BCM) - 1]:
            pinTrue = bool(address >> i & 1)
            pinBcm = self.INPUT_SELECTOR_BCM[i]
            self.__gpio.output(pinBcm, self.__gpio.LOW if pinTrue else self.__gpio.HIGH)

    def __play_stream(self, url):
        p = Popen(["mpg123", url])
        self.__stream_play_processes.append(p)


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
