import requests
import time
import json

server_address = 'http://localhost:8080/AudioController/api/v1/controller'
# server_address = 'http://192.168.1.43:8080/AudioController/api/v1'
json_enable = '{"Enabled": true}'
json_disable = '{"Enabled": false}'

print(requests.put(server_address,'{"SelectedInput": 2}').json())
print(requests.get(server_address).json())
print(requests.get(server_address + '/zones').json())
time.sleep(1)
print(requests.put(server_address + '/zones/1',json_enable).json())
time.sleep(1)
print(requests.put(server_address + '/zones/2',json_enable).json())
time.sleep(1)
print(requests.put(server_address + '/zones/3',json_enable).json())
time.sleep(1)
print(requests.put(server_address + '/zones/1',json_disable).json())
time.sleep(1)
print(requests.put(server_address + '/zones/2',json_disable).json())
time.sleep(1)
print(requests.put(server_address + '/zones/3',json_disable).json())
time.sleep(1)
print(requests.put(server_address,'{"SelectedInput": 2}').json())
time.sleep(1)
print(requests.put(server_address,'{"SelectedInput": 3}').json())
time.sleep(1)
print(requests.put(server_address,'{"SelectedInput": 1}').json())

#
# jsonstring = '{"Enabled": true}'
# time.sleep(2)
# response = requests.put('http://localhost:8080/zones/1', jsonstring)
# data = response.json()
#
# response = requests.put('http://localhost:8080/zones/3', jsonstring)
# data = response.json()
