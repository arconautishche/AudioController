import json
import web
import urllib.parse
from logging import info, debug, error
import sys

base_url = '/AudioController/api/v1/controller'

urls = (
    base_url, 'Controller',
    base_url + '/inputs', 'Inputs',
    base_url + '/zones', 'Zones',
    base_url + '/zones/(.*)', 'Zone'
)


def start_service(ac):
    sys.argv = [sys.argv[0]]  # remove all arguments as they would be interpreted as arguments by app.run() call
    app = web.application(urls, globals())
    web.audio_controller = ac # 'hack' to keep singleton audiocontroller context
    app.add_processor(error_catcher)
    app.run()

def set_headers():
    web.header('Content-Type', 'application/json')
    web.header('Access-Control-Allow-Origin', '*')
    web.header('Access-Control-Allow-Credentials', 'true')

class Zone:
    def GET(self, zone):
        zone = web.audio_controller.zones[int(zone)]
        set_headers()
        return json.dumps(construct_zone(zone))

    def PUT(self, zone):
        data = web.data().decode('ascii')
        zone_id = int(zone)
        set_headers()
        return_object = update_zone(zone_id, data)
        return json.dumps(return_object)

    def OPTIONS(self, zone):
        debug("OPTIONS REQUESTED")
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', 'GET,PUT')
        web.header('Access-Control-Allow-Credentials', 'true')
        return

class Zones:
    def GET(self):
        zones = web.audio_controller.zones
        set_headers()
        return json.dumps(construct_zones(zones))


class Inputs:
    def GET(self):
        inputs = web.audio_controller.inputs
        set_headers()
        return json.dumps(construct_inputs(inputs))


class Controller:
    def GET(self):
        set_headers()
        return_object = construct_controller(web.audio_controller)
        return json.dumps(return_object)

    def PUT(self):
        data = web.data().decode('ascii')
        set_headers()
        return json.dumps(update_controller(web.audio_controller, data))

    def OPTIONS(self):
        debug("OPTIONS REQUESTED")
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', 'GET,PUT')
        web.header('Access-Control-Allow-Credentials', 'true')
        return


def construct_zone(zone):
    zone_dto = {'ZoneId': zone.id,
             'Name': zone.name,
             'Enabled': zone.enabled}
    return zone_dto


def construct_zones(zones):
    zones_constructed = []
    for _, zone in zones.items(): zones_constructed.append(construct_zone(zone))
    return zones_constructed


def construct_controller(audio_controller):
    return ({'Inputs': construct_inputs(audio_controller.inputs),
             'Zones': construct_zones(audio_controller.zones),
             'SelectedInput': audio_controller.selected_input,
             'MasterVolume': audio_controller.master_volume,
             })

def construct_inputs(inputs):
    return [construct_input(inp_id, inp) for inp_id, inp in inputs.items()]


def construct_input(inp_id, inp):
    input_dto = {
        'InputId': inp_id,
        'Name': inp.name,
        'Group': inp.group
    }
    if inp.icon: input_dto['icon'] = urllib.parse.urljoin(urllib.parse.urljoin(web.ctx.homedomain, "/static/"), inp.icon)
    return input_dto


def update_zone(zone_id, data):
    info("updating zone. data received: {}".format(data))
    parsed_data = json.loads(data)
    if 'Enabled' in parsed_data:
        web.audio_controller.set_zone_enabled(zone_id, parsed_data['Enabled'])
    return construct_zone(web.audio_controller.zones[zone_id])


def update_controller(controller, data):
    parsed_data = json.loads(data)
    if 'MasterVolume' in parsed_data:
        controller.master_volume = max(min(int(parsed_data['MasterVolume']), 100), 0)
    if 'SelectedInput' in parsed_data:
        controller.select_input(parsed_data['SelectedInput'])
    return {'SelectedInput': controller.selected_input}

def error_catcher(handler):
    try:
        return handler()
    except Exception as e:
        error("Audiocontroller Exception occurred")
        error(str(e))
        return e