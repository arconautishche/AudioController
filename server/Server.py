from AudioController import AudioController
import Config
import RestService
from logging import info

def start_server():
    print('starting service...')
    print('loading config...')
    Config.load()
    info("Config loaded")

    ac = AudioController()
    RestService.start_service(ac)


start_server()
