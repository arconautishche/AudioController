import web
import json
from AudioController import AudioController


class AudioRestService:
    urls = (
        '/AudioController/api/v1/controller', 'Controller',
        '/AudioController/api/v1/controller/inputs', 'Inputs',
        '/AudioController/api/v1/controller/zones', 'Zones',
        '/AudioController/api/v1/controller/zones/(.*)', 'Zone'
    )

    def start_service(self, ac):
        app = web.application(self.urls, globals())
        web.audio_controller = ac
        app.run()


class Zone:
    def GET(self, zone):
        zone = web.audio_controller.zones[int(zone)]
        web.header('Content-Type', 'application/json')
        return json.dumps(construct_zone(zone))

    def PUT(self, zone):
        data = web.data()
        zone = web.audio_controller.zones[int(zone)]
        web.header('Content-Type', 'application/json')
        return json.dumps(update_zone(zone, data))


class Zones:
    def GET(self):
        zones = web.audio_controller.zones
        web.header('Content-Type', 'application/json')
        return json.dumps(construct_zones(zones))


class Inputs:
    def GET(self):
        inputs = web.audio_controller.inputs
        web.header('Content-Type', 'application/json')
        return json.dumps(construct_inputs(inputs))


class Controller:
    def GET(self):
        web.header('Content-Type', 'application/json')
        return json.dumps(construct_controller(web.audio_controller))

    def PUT(self):
        data = web.data()
        web.header('Content-Type', 'application/json')
        return json.dumps(update_controller(web.audio_controller, data))


def construct_zone(zone):
    return ({'ZoneId': zone.id, \
             'Name': zone.name, \
             'Enabled': zone.on})


def construct_zones(zones):
    zones_constructed = []
    for zone_id, zone in zones.items(): zones_constructed.append(construct_zone(zone))
    return zones_constructed


def construct_controller(audio_controller):
    return ({'Inputs': construct_inputs(audio_controller.inputs), \
             'Zones': construct_zones(audio_controller.zones), \
             'SelectedInput': audio_controller.selected_input})
    for zoneid, zone in zones.items(): zones_constructed.append(construct_zone(zone))
    return zones_constructed


def construct_inputs(inputs):
    inputs_constructed = []
    for inp_id, inp in inputs.items(): inputs_constructed.append(construct_input(inp_id, inp))
    return inputs_constructed


def construct_input(inp_id, inp):
    return ({'InputId': inp_id, \
             'Name': inp.name})


def update_zone(zone, data):
    parsed_data = json.loads(data)
    zone.set_enabled(parsed_data['Enabled'])
    return construct_zone(zone)


def update_controller(controller, data):
    parsed_data = json.loads(data)
    controller.select_input(parsed_data['SelectedInput'])
    return {'SelectedInput': controller.selected_input}
