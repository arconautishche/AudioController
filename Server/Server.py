from AudioController import AudioController
import json
import logging

import RestService

def StartServer(gpio, volume_control=None):
    print('starting service...')
    print('loading config...')
    with open("config.json") as file:
        config = json.loads(file.read())

    if "log_level" in config:
        logging.basicConfig()
        logging.getLogger().setLevel(config["log_level"])

    ac = AudioController(gpio, volume_control)
    RestService.start_service(ac)