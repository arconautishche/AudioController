import time

import requests

server_address = 'http://localhost:8080/AudioController/api/v1/controller'
# server_address = 'http://192.168.1.43:8080/AudioController/api/v1/controller'
json_enable = '{"Enabled": true}'
json_disable = '{"Enabled": false}'


def get_zones():
    print(requests.get(server_address).json())


def set_zone(zone_id, enabled=True, wait=1):
    json = json_enable if enabled else json_disable
    print(requests.put('{}/zones/{}'.format(server_address, zone_id), json).json())
    time.sleep(wait)


def enable_zone(zone_id, wait=1):
    set_zone(zone_id, True, wait)


def disable_zone(zone_id, wait=1):
    set_zone(zone_id, False, wait)


def select_input(input_id, wait=1):
    print(requests.put(server_address, '{{"SelectedInput": {}}}'.format(input_id)).json())
    time.sleep(wait)


get_zones()
enable_zone(0)
enable_zone(1)
enable_zone(2)
disable_zone(0)
disable_zone(1)
disable_zone(2)

select_input(0)
select_input(1)
select_input(0)
select_input(2)
# select_input(2)
# select_input(3)
# select_input(4)
# select_input(5)
