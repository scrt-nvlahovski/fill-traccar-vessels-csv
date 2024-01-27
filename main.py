import os

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
URL, MAIL, PASS = def_config

traccar = TraccarApi(URL, MAIL, 'PASS')
try:
    traccar.login()
except TraccarApiAuthenticationError as e:
    print(f"Authentication error: {e}")
except TraccarApiError as e:
    print(f"API error: {e}")

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
print()
