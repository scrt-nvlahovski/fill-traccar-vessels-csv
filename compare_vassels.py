import json, os
from external_services.traccar_api.api import TraccarApi
from external_services.traccar_api.traccar_errors.traccar_api_errors import *
from helpers.common import search_list_dicts, search_vessel_attribute

prod_config = [
    os.environ.get("TRACCAR_URL_PROD"),
    os.environ.get("TRACCAR_MAIL_PROD"),
    os.environ.get("TRACCAR_PASS_PROD")
]

URL, MAIL, PASS = prod_config

fvms = None
eafa = None
matches = []
lost = []
found_errors = []
traccar_api = TraccarApi(URL, MAIL, PASS)

with open("external_files/datas/fvms-vessel.json") as file:
    fvms = json.load(file)

if fvms:
    user = traccar_api.login()
    eafa = traccar_api.get_devices()

    # if eafa and fvms:
    #     for eafa_vessel in eafa:
    #         if "cfr" in eafa_vessel['attributes'] and not eafa_vessel['attributes']['cfr'] is None:
    #             match = search_list_dicts("cfr", eafa_vessel['attributes']['cfr'], fvms)
    #             if len(match) > 0:
    #                 matches.append((match[0], eafa_vessel))
    #             else:
    #                 lost.append(eafa_vessel)

    found_errors = []

    for match, vessel in matches:
        if not match['uniqueid'] == vessel['uniqueId']:
            found_errors.append((match, vessel))


def del_element_list_dict(attribute: str, value: any, data: list):
    for element in data.copy():
        if element[attribute] == value:
            del element[attribute]


found_errors = []
if eafa is not None and fvms is not None:
    for fvms_vessel in fvms:
        if "cfr" in fvms_vessel and not fvms_vessel['cfr'] is '':
            match = search_vessel_attribute("cfr", fvms_vessel['cfr'], eafa)
            if match and len(match) > 0:
                print()
            else:
                found_errors.append(fvms_vessel)

attributes = {"cfr": "BGR001010393", "idp": "01442528SKY7C9D", "ip": "10.10.20.87", "ext": "ВН 393", "name": "TAIS",
              "length": "13.5", "width": "5.6", "mmsi": "207293000", "owner": "ЕЛЕКТА ЕООД ", "email": "",
              "captain": "Николай Димов Добрев", "deep": 1.7, "gt": 46, "fvms": "3.0.0.9.1", "cyrName": "ТАИС",
              "callSign": "LZH SU", "companyAddress": "гр. Варна, ул. Братя Георгиевич 15, вх.А, ап.11",
              "contactPhone": "878399736", "portHome": "BGVAR", "portStay": "BGVAR", "height": "1.98"}

tais = traccar_api.get_device(device_unique_ids="01442528SKY7C9D")
if tais is not None:
    tais= tais[0]

tais['attributes'] = attributes
# traccar_api.update_device(tais)

traccar_api.logout()
