import csvimport jsonimport warningsimport requestsfrom requests.auth import HTTPBasicAuthfrom requests_pkcs12 import getfrom helpers.common import transliterate_bulgarian_to_englishfrom models.devivce_attribute import DeviceAttributewarnings.filterwarnings('ignore', message='Unverified HTTPS request')attributes = []csv_file_path = 'data/vessels.csv'data = []with open(csv_file_path, mode='r', encoding='utf-8') as file:    csv_reader = csv.reader(file)    next(csv_reader)    for row in csv_reader:        data.append(row)for row in data:    attribute = DeviceAttribute()    call_sign = mmsi = ""    cfr, idp, ip, external_marking, ship_name, length, width, call_sign_mmsi, ship_owner, company_address, email, captain, contact_phone = row    try:        call_sign, mmsi = str(call_sign_mmsi).split("/")    except Exception:        call_sign = call_sign_mmsi    attribute.cfr = cfr    attribute.idp = idp    attribute.ip = ip    attribute.ext = external_marking    attribute.cyr_name = ship_name    attribute.name = transliterate_bulgarian_to_english(ship_name)    attribute.length = length    attribute.width = width    attribute.callSign = call_sign    attribute.mmsi = mmsi    attribute.owner = ship_owner    attribute.companyAddress = company_address    attribute.email = email    attribute.captain = captain    attribute.contactPhone = contact_phone    attributes.append(attribute)def do_get(uri: str):    url = uri    headers = {'Accept': 'application/json'}    try:        response1 = get("https://bkmonitor.apps.scrtl.xyz/v1/api/vessels/active",                        headers=headers,                        verify=False,                        pkcs12_filename="/Users/nvl/Documents/Secure/bkmonitor/bkmonitor.apps.scrtl.xyz.p12",                        pkcs12_password="hpv6q9")        return response1.json()    except Exception as e:        return edef get_single_vessel_traccar(uniqueId):    url = 'http://127.0.0.1:8082/api/devices'    params = {'uniqueId': uniqueId}    auth = HTTPBasicAuth('n.vlahovski@scortel.com', 'admin')    response = requests.get(url, headers={'Accept': 'application/json'}, auth=auth, params=params)    if response.status_code == 200:        return response.json()[0] if len(response.json()) > 0 else {}    else:        return {}def prepare_add_vessel_traccar(vessel):    new_vessel = {        "id": 0,        "name": str(vessel.cyr_name).upper(),        "uniqueId": str(vessel.idp).upper(),        "status": "",        "disabled": False,        "lastUpdate": "",        "positionId": 0,        "groupId": 1,        "phone": str(vessel.contact_phone).upper(),        "model": "",        "contact": str(vessel.owner).upper(),        "category": "boat",        "attributes": vessel.to_dict()    }    return new_vesseldef update_vessel_traccar(vessel):    url = f'http://127.0.0.1:8082/api/devices/{vessel["id"]}'    auth = HTTPBasicAuth('n.vlahovski@scortel.com', 'birka24')    response = requests.put(url, headers={'Content-Type': 'application/json'}, auth=auth, json=vessel)    if response.status_code == 200:        return response.json() if len(response.json()) > 0 else {}    else:        return {}    passdef add_vessel_traccar(vessel):    url = f'http://127.0.0.1:8082/api/devices/'    auth = HTTPBasicAuth('n.vlahovski@scortel.com', 'admin')    response = requests.post(url, headers={'Content-Type': 'application/json'}, auth=auth, json=vessel)    if response.status_code == 200:        return response.json() if len(response.json()) > 0 else {}    else:        return {}    passdef prepare_update_vessel_traccar(vessel):    traccar_vessel = get_single_vessel_traccar(vessel.idp)    if traccar_vessel:        traccar_vessel['attributes'] = vessel.to_dict()        return traccar_vesseluri = f"/vessels/active"dicts: list = do_get(uri)for attribute in attributes:    matched_vessel = next((d for d in dicts if d['CFR'] == attribute.cfr), None)    if matched_vessel:        attribute.idp = matched_vessel['IDP']        attribute.ip = matched_vessel['IP']        attribute.deep = matched_vessel['deep']        attribute.gt = matched_vessel['gt']        attribute.fvms = matched_vessel['fvms']for vessel in attributes:    ready_vessel = prepare_update_vessel_traccar(vessel)    if ready_vessel:        update_vessel_traccar(ready_vessel)    else:        ready_vessel = prepare_add_vessel_traccar(vessel)        if ready_vessel:            add_vessel_traccar(ready_vessel)    print(ready_vessel)