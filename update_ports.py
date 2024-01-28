import os

from external_services.nafa_api.api import NafaApi
from external_services.nafa_api.nafa_api_errors.nafa_api_errors import NafaApiAuthenticationError, NafaApiError
from external_services.traccar_api.api import TraccarApi
from external_services.traccar_api.traccar_errors.traccar_api_errors import *
from helpers.common import validate_phone_number


def get_captains_list(drivers_list: list) -> list:
    captains_list = []
    for person in drivers_list:
        if 'isCaptain' in person['attributes'] and person['attributes']['isCaptain'] is True:
            captains_list.append(person)
    return captains_list


def get_captain_device(captains_list: list, device_list: list) -> list:
    pears = []
    for captain in captains_list:
        captain_id = captain['uniqueId']
        for device_object in device_list:
            if 'contactPhone' in device_object['attributes'] and validate_phone_number(
                    device_object['attributes']['contactPhone']) == captain_id:
                pears.append((captain['id'], device_object['id']))
    return pears


def set_device_category(device_object: dict) -> dict:
    if 'length' in device_object['attributes']:
        if float(device_object['attributes']['length']) > 14.99:
            category = "ship"
        else:
            category = "boat"
    else:
        category = "default"
    if device_object['category'] != category:
        device_object['category'] = category

    return device_object


def check_device_attributes_name(device_object: dict) -> dict:
    if 'attributes' in device_object:
        for attribute, value in device_object['attributes'].copy().items():
            attribute_name_list = attribute.split('_')
            if len(attribute_name_list) > 1:
                new_attribute_name = attribute_name_list[0] + str(attribute_name_list[1]).capitalize()
                if new_attribute_name not in device_object['attributes']:
                    device_object['attributes'][new_attribute_name] = value
                    del device_object['attributes'][attribute]
    return device_object


local_config = [
    "http://127.0.0.1:8082",
    "n.vlahovski@scortel.com",
    "admin"
]

def_config = [
    os.environ.get("TRACCAR_URL_DEV"),
    os.environ.get("TRACCAR_MAIL_DEV"),
    os.environ.get("TRACCAR_PASS_DEV")
]
prod_config = [
    os.environ.get("TRACCAR_URL_PROD"),
    os.environ.get("TRACCAR_MAIL_PROD"),
    os.environ.get("TRACCAR_PASS_PROD")
]
URL, MAIL, PASS = prod_config
current_user = None
traccar = TraccarApi(URL, MAIL, PASS)
traccar_dev = TraccarApi(*def_config)
traccar_dev_user = traccar_dev.login()
nafa = NafaApi("http://iss.iara.government.bg/scrtl", "nvl.api@scortel.com", "2JHAFy3yeXu6gKNK")
try:
    current_user = traccar.login()
except TraccarApiAuthenticationError as e:
    print(f"Authentication error: {e}")
except TraccarApiError as e:
    print(f"API error: {e}")

try:
    nafa.login()
except NafaApiAuthenticationError as e:
    print(f"Authentication error: {e}")
except NafaApiError as e:
    print(f"API error: {e}")

vessels_list = traccar.get_devices()

for vessel in vessels_list:
    if "cfr" in vessel["attributes"]:
        nafa_vessel = None
        try:
            nafa_vessel = nafa.get_vessel(cfr=vessel["attributes"]["cfr"])
        except NafaApiAuthenticationError as e:
            print(f"Authentication error: {e}")
        except NafaApiError as e:
            print(f"API error: {e}")
        if nafa_vessel:
            height = nafa_vessel["height"] if "height" in nafa_vessel else None
            port_home = nafa_vessel["port_home"] if "port_home" in nafa_vessel else None
            port_stay = nafa_vessel["port_stay"] if "port_stay" in nafa_vessel else None
            port_id = nafa_vessel["port_id"] if "port_id" in nafa_vessel else -1
            stay_id = nafa_vessel["stay_id"] if "stay_id" in nafa_vessel else -1
            if not port_home and port_id > 0:
                port_homes = traccar_dev.get_ports(port_ids=[nafa_vessel["port_id"]])
                port_stay = port_homes[0] if len(port_homes) > 0 else None
            if not port_stay and stay_id > 0:
                port_stays = traccar_dev.get_ports(port_ids=[nafa_vessel["stay_id"]])
                port_stay = port_stays[0] if len(port_stays) > 0 else None
            vessel["attributes"]["height"] = height if height is not None else -1
            vessel["attributes"]["portHome"] = port_home if port_home is not None else ""
            vessel["attributes"]["portStay"] = port_stay if port_stay is not None else ""

for vessel in vessels_list:
    print(traccar.update_device(vessel))
    print()

# nafa_vessel = nafa.get_vessel(cfr="BGR001028535")

# current_user = traccar.login()

# Bulks
# server = traccar.get_server()
# devices = traccar.get_devices()
# devices_criteria = traccar.get_device(device_ids=[3, 38], device_unique_ids=["01442517SKYD066", "01433630SKYC6D3"])
# users = traccar.get_users()
# drivers = traccar.get_drivers()
# groups = traccar.get_groups()
# # Singles
# device = traccar.get_device(device_unique_ids=["01433630SKYC6D3"])
# user = traccar.get_user(1)
# driver = traccar.get_driver(301)
# # Resources
# resources = traccar.get_current_user_resources()
# # Links
# link_driver1_device1 = traccar.link_diver_device(driver_id=301, device_id=3)
# link_driver2_device1 = traccar.link_diver_device(driver_id=302, device_id=3)
# unlink_driver1_device1 = traccar.unlink_diver_device(driver_id=301, device_id=3)
# unlink_driver2_device1 = traccar.unlink_diver_device(driver_id=302, device_id=3)

# Errors
# test_errors = traccar.test_error()

# LogOut

# captains = get_captains_list(drivers)

# captain_devices = get_captain_device(captains, devices)

# for captain_id, device_id in captain_devices:
#     traccar.link_diver_device(driver_id=captain_id, device_id=device_id, )

# for device in devices:
#     set_device_category(device)
#     check_device_attributes_name(device)
#     # print(traccar.update_device(device))
try:
    traccar.logout()
except TraccarApiAuthenticationError as e:
    print(f"Authentication error: {e}")
except TraccarApiError as e:
    print(f"API error: {e}")

try:
    nafa.logout()
except NafaApiAuthenticationError as e:
    print(f"Authentication error: {e}")
except NafaApiError as e:
    print(f"API error: {e}")
print()
