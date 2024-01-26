import os

from external_services.traccar_api.api import TraccarApi
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
        for device in device_list:
            if 'contact_phone' in device['attributes'] and validate_phone_number(
                    device['attributes']['contact_phone']) == captain_id:
                pears.append((captain['id'], device['id']))
    return pears


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

# URL = "https://iara-prior-notification.scrtl.xyz"
# MAIL = "n.vlahovski@scortel.com"
# PASS = "admin"

traccar = TraccarApi(URL, MAIL, PASS)

current_user = traccar.login()

# Bulks
# server = traccar.get_server()
devices = traccar.get_devices()
# devices_criteria = traccar.get_device(device_ids=[3, 38], device_unique_ids=["01442517SKYD066", "01433630SKYC6D3"])
# users = traccar.get_users()
drivers = traccar.get_drivers()
# groups = traccar.get_groups()
# # Singles
# device = traccar.get_device(device_unique_ids=["01433630SKYC6D3"])
# user = traccar.get_user(1)
# driver = traccar.get_driver(301)
# # Permissions
# permissions = traccar.get_current_user_permissions()
# link_driver1_device1 = traccar.link_diver_device(driver_id=301, device_id=3)
# link_driver2_device1 = traccar.link_diver_device(driver_id=302, device_id=3)
# unlink_driver1_device1 = traccar.unlink_diver_device(driver_id=301, device_id=3)
# unlink_driver2_device1 = traccar.unlink_diver_device(driver_id=302, device_id=3)

# Errors
# test_errors = traccar.test_error()

# LogOut

captains = get_captains_list(drivers)

captain_devices = get_captain_device(captains, devices)

# for captain_id, device_id in captain_devices:
#     traccar.link_diver_device(driver_id=captain_id, device_id=device_id, )

traccar.logout()

print()
