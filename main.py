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
vessel_dict = None
captain = None

traccar = TraccarApi(*def_config)

try:
    current_user = traccar.login()
except TraccarApiAuthenticationError as e:
    print(f"Authentication error: {e}")
except TraccarApiError as e:
    print(f"API error: {e}")
if current_user:
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

    vessel.name = vessel_dict["name"] if vessel_dict["name"] else ""
    vessel.id = vessel_dict["id"] if vessel_dict["id"] else ""
    vessel.uniqueId = vessel_dict["uniqueId"] if vessel_dict["uniqueId"] else ""
    vessel.status = vessel_dict["status"] if vessel_dict["status"] else ""
    vessel.disabled = vessel_dict["disabled"] if vessel_dict["disabled"] else True
    vessel.lastUpdate = vessel_dict["lastUpdate"] if vessel_dict["lastUpdate"] else None
    vessel.positionId = vessel_dict["positionId"] if vessel_dict["positionId"] else -1
    vessel.groupId = vessel_dict["groupId"]  if vessel_dict["groupId"] else -1
    vessel.phone = vessel_dict["phone"] if vessel_dict["phone"] else ""
    vessel.model = vessel_dict["model"] if vessel_dict["model"] else ""
    vessel.contact = vessel_dict["contact"] if vessel_dict["contact"] else ""
    vessel.category = vessel_dict["category"] if vessel_dict["category"] else ""
    for attribute, value in vessel_dict["attributes"].items():
        vessel.set(attribute, value)
    if "attributes" in captain and "isCaptain" in captain['attributes'] and captain['attributes']['isCaptain'] is True:
        vessel.set("captain",
                   {
                        "id": captain["id"],
                        "uniqueId": validate_phone_number(captain["uniqueId"]),
                        "name": captain["name"],
                        "nameEn": captain["attributes"]["nameEn"]
                        }
                   )
print(vessel.get("ip"))
print(vessel.getOrDefault("captain", {"captain": {}}))
print(vessel.to_dict())
