from AudioController import AudioController
import logging
import Config
from Config import config

import RestService


def start_server():
    print('starting service...')
    Config.load()
    print(config())

    print('loading config...')

    if "log_level" in config():
        logging.basicConfig()
        logging.getLogger().setLevel(config()["log_level"])

    ac = AudioController()
    RestService.start_service(ac)


start_server()
