import csvimport warningsimport requestsfrom requests.auth import HTTPBasicAuthfrom helpers.common import transliterate_bulgarian_to_english, validate_phone_numberfrom models.inspector import Inspectorfrom pathlib import Pathwarnings.filterwarnings('ignore', message='Unverified HTTPS request')inspectors = []root_dir = Path.joinpath(Path(__file__).parent.parent.parent, 'data')csv_file_path =  Path.joinpath(root_dir, 'inspectors.csv')data = []def add_driver_traccar(driver):    url = f'https://fvmspnc.iara.government.bg/api/drivers/'    auth = HTTPBasicAuth('n.vlahovski@scortel.com', 'birka24')    response = requests.post(url, headers={'Content-Type': 'application/json'}, auth=auth, json=driver.to_dict())    if response.status_code == 200:        return response.json() if len(response.json()) > 0 else {}    else:        return {}with open(csv_file_path, mode='r', encoding='utf-8') as file:    csv_reader = csv.reader(file)    next(csv_reader)    for row in csv_reader:        data.append(row)for row in data:    title, fullName, phone, email, cardId = row    inspector = Inspector()    inspector.name = fullName    inspector.uniqueId = cardId    inspector.set("isInspector", True)    inspector.set("phone", validate_phone_number(phone.replace(' ', '')))    inspector.set("title", title)    inspector.set("email", email)    inspector.set("nameEn", transliterate_bulgarian_to_english(fullName))    inspectors.append(inspector)for inspector in inspectors:    add_driver_traccar(inspector)