import os

from external_services.traccar_api.api import TraccarApi
from external_services.traccar_api.traccar_errors.traccar_api_errors import *
from helpers.common import validate_phone_number
from models.vessel import Vessel


local_config = [
    "http://127.0.0.1:8082",
    os.environ.get("TRACCAR_MAIL_DEV"),
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
traccar = TraccarApi(*def_config)

try:
    current_user = traccar.login()
except TraccarApiAuthenticationError as e:
    print(f"Authentication error: {e}")
except TraccarApiError as e:
    print(f"API error: {e}")

vessel_dict = traccar.get_device(device_unique_ids=["01442545SKY40F2"])[0]
captain = traccar.get_drivers(device_ids=[vessel_dict["id"]])[0]
vessel_dict["captain"] = captain
try:
    traccar.logout()
except TraccarApiAuthenticationError as e:
    print(f"Authentication error: {e}")
except TraccarApiError as e:
    print(f"API error: {e}")

vessel = Vessel()

if vessel_dict:

    vessel.name = vessel_dict["name"]
    vessel.id = vessel_dict["id"]
    vessel.uniqueId = vessel_dict["uniqueId"]
    vessel.status = vessel_dict["status"]
    vessel.disabled = vessel_dict["disabled"]
    vessel.lastUpdate = vessel_dict["lastUpdate"]
    vessel.positionId = vessel_dict["positionId"]
    vessel.groupId = vessel_dict["groupId"]
    vessel.phone = vessel_dict["phone"]
    vessel.model = vessel_dict["model"]
    vessel.contact = vessel_dict["contact"]
    vessel.category = vessel_dict["category"]
    for attribute, value in vessel_dict["attributes"].items():
        vessel.set(attribute, value)
    if "isCaptain" in captain['attributes'] and captain['attributes']['isCaptain'] is True:
        vessel.set("captain",
                   {
                        "id": captain["id"],
                        "uniqueId": validate_phone_number(captain["uniqueId"]),
                        "name": captain["name"],
                        "nameEn": captain["attributes"]["nameEn"]
                        }
                   )

print(vessel.to_dict())
