import requests
import json
from time import sleep

server_address = 'http://localhost:8080/AudioController/api/v1/controller'
# server_address = 'http://192.168.1.43:8080/AudioController/api/v1/controller'
json_enable = '{"Enabled": true}'
json_disable = '{"Enabled": false}'


def get_zones():
    print(requests.get(server_address).json())


def set_zone(zone_id, enabled=None, volume=None, wait=1):
    payload = {}
    if enabled is not None:
        payload['Enabled'] = enabled
    if volume is not None:
        payload['Volume'] = volume
    payload_str = json.dumps(payload)
    response = requests.put('{}/zones/{}'.format(server_address, zone_id), payload_str)
    try:
        print(response.json())
    except:
        print(response)
    sleep(wait)


def enable_zone(zone_id, wait=1):
    set_zone(zone_id, True, wait=wait)


def disable_zone(zone_id, wait=1):
    set_zone(zone_id, False, wait=wait)


def set_volume(zone_id, volume):
    set_zone(zone_id, volume=volume)


def select_input(input_id, wait=1):
    response = requests.put(server_address, '{{"SelectedInput": {}}}'.format(input_id))
    try:
        print(response.json())
    except:
        print(response)
    sleep(wait)


def volume_loop(low, high, period):
    assert low < high
    steps = list(range(low, high)) + list(range(high, low))
    sleep_time = period / len(steps)
    while True:
        for volume in steps:
            set_volume(0, volume)
            sleep(sleep_time)


get_zones()

# select_input(0)
# select_input(2)
select_input(2)
# select_input(3)
# select_input(4)
# select_input(5)

enable_zone(0)
enable_zone(1)
disable_zone(0)
enable_zone(2)
disable_zone(1)
disable_zone(2)

# set_volume(0, 133)
