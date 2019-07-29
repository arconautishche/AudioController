import requests
import time
import json

# server_address = 'http://localhost:8080/AudioController/api/v1/controller'
server_address = 'http://192.168.1.43:8080/AudioController/api/v1/controller'
json_enable = '{"Enabled": true}'
json_disable = '{"Enabled": false}'

def get_zones():
    print(requests.get(server_address).json())

def select_zone(zone_id, enabled=True, wait=1):
    json = json_enable if enabled else json_disable
    print(requests.put('{}/zones/{}'.format(server_address, zone_id), json).json())
    time.sleep(wait)

def select_input(input_id, wait=1):
    print(requests.put(server_address, '{{"SelectedInput": {}}}'.format(input_id)).json())
    time.sleep(wait)

get_zones()
select_zone(1, True)
select_zone(2, True)
select_zone(3, True)
select_zone(1, False)
select_zone(2, False)
select_zone(3, False)

# select_input(0)
select_input(1)
select_input(2)
select_input(3)
select_input(4)
select_input(5)

