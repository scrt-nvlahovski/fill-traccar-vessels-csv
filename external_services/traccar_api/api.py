import warnings

import requests
from requests.auth import HTTPBasicAuth


warnings.filterwarnings('ignore', message='Unverified HTTPS request')
warnings.filterwarnings('ignore', message='NotOpenSSLWarning')


class TraccarApi:
    def __init__(self, traccar_api_url: str, traccar_api_mail: str, traccar_api_pass: str):
        self.__traccar_api_url = traccar_api_url
        self.__traccar_api_mail = traccar_api_mail
        self.__traccar_api_pass = traccar_api_pass
        self.__traccar_api_session = None
        self.__traccar_api_session = requests.Session()
        self.__traccar_api_token = None

    def get_traccar_api_url(self):
        return self.__traccar_api_url

    def get_traccar_api_mail(self):
        return self.__traccar_api_mail

    def get_traccar_api_pass(self):
        return self.__traccar_api_pass

    def set_traccar_api_url(self, traccar_api_url: str) -> None:
        self.__traccar_api_url = traccar_api_url

    def set_traccar_api_mail(self, traccar_api_mail: str) -> None:
        self.__traccar_api_mail = traccar_api_mail

    def set_traccar_api_pass(self, traccar_api_pass: str) -> None:
        self.__traccar_api_pass = traccar_api_pass

    def set_traccar_api_token(self, token: str) -> None:
        self.__traccar_api_token = token

    def login(self):
        login_url = f"{self.__traccar_api_url}/api/session"
        self.__traccar_api_session.auth = HTTPBasicAuth(self.__traccar_api_mail, self.__traccar_api_pass)
        login_data = {
            'email': self.__traccar_api_mail,
            'password': self.__traccar_api_pass
        }
        response = self.__traccar_api_session.post(login_url, data=login_data)

        if response.status_code == 200:
            print('Login successful')
            cookies = self.__traccar_api_session.cookies.get_dict()
            self.set_traccar_api_token(cookies['JSESSIONID'])
            return response.json()
        else:
            print(f'Login failed with status code: {response.status_code}')
            return None

    def logout(self):
        logout_url = f"{self.__traccar_api_url}/api/session"
        if self.__traccar_api_session is not None:
            response = self.__traccar_api_session.delete(logout_url)
            if response.status_code == 204:
                print('Logout successful')
                self.__traccar_api_session = None
                self.set_traccar_api_token(None)
            else:
                print(f'ERROR: {response.status_code} - {response.text}')
        else:
            print(f'Error: missing session')
            return None

    def get_devices(self):
        url = f"{self.__traccar_api_url}/api/devices"
        if self.__traccar_api_session is not None:
            response = self.__traccar_api_session.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f'ERROR: {response.status_code} - {response.text}')
                return []
        else:
            print(f'Error: missing session')
            return None

    def get_device(self, *, device_ids: list = None, device_unique_ids: list = None, user_id: int = None):
        url = f"{self.__traccar_api_url}/api/devices"
        params = {}

        if user_id is not None:
            params['userId'] = user_id
        if device_ids:
            params['id'] = device_ids
        if device_unique_ids:
            params['uniqueId'] = device_unique_ids

        if self.__traccar_api_session is not None:
            response = self.__traccar_api_session.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print(f'ERROR: {response.status_code} - {response.text}')
                return []
        else:
            print(f'Error: missing session')
            return None

    def get_users(self):
        url = f"{self.__traccar_api_url}/api/users"
        if self.__traccar_api_session is not None:
            response = self.__traccar_api_session.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f'ERROR: {response.status_code} - {response.text}')
                return []
        else:
            print(f'Error: missing session')
            return None

    def get_user(self, user_id):
        url = f"{self.__traccar_api_url}/api/users/{user_id}"
        if self.__traccar_api_session is not None:
            response = self.__traccar_api_session.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f'ERROR: {response.status_code} - {response.text}')
                return []
        else:
            print(f'Error: missing session')
            return None

    def get_server(self):
        url = f"{self.__traccar_api_url}/api/server"
        if self.__traccar_api_session is not None:
            response = self.__traccar_api_session.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f'ERROR: {response.status_code} - {response.text}')
                return []
        else:
            print(f'Error: missing session')
            return None

    def get_drivers(self):
        url = f"{self.__traccar_api_url}/api/drivers"
        if self.__traccar_api_session is not None:
            response = self.__traccar_api_session.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f'ERROR: {response.status_code} - {response.text}')
                return []
        else:
            print(f'Error: missing session')
            return None

    def get_driver(self, driver_id: int):
        url = f"{self.__traccar_api_url}/api/drivers/{driver_id}"
        if self.__traccar_api_session is not None:
            response = self.__traccar_api_session.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f'ERROR: {response.status_code} - {response.text}')
                return []
        else:
            print(f'Error: missing session')
            return None

    def get_groups(self):
        url = f"{self.__traccar_api_url}/api/groups"
        if self.__traccar_api_session is not None:
            response = self.__traccar_api_session.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f'ERROR: {response.status_code} - {response.text}')
                return []
        else:
            print(f'Error: missing session')
            return None

    def test_error(self):
        url = f"{self.__traccar_api_url}/api/permissions"
        if self.__traccar_api_session is not None:
            response = self.__traccar_api_session.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f'ERROR: {response.status_code} - {response.text}')
                return []
        else:
            print(f'Error: missing session')
            return None

    def get_current_user_permissions(self):
        groups = self.get_groups()
        devices = self.get_devices()
        users = self.get_users()
        drivers = self.get_drivers()

        return {
            'groups': groups,
            'devices': devices,
            'users': users,
            'drivers': drivers
        }

    def link_device_user(self, *, device_id, user_id):
        url = f"{self.__traccar_api_url}/api/permissions"
        params = {"userId": user_id, "deviceId": str(device_id)}
        if self.__traccar_api_session is not None:
            response = self.__traccar_api_session.post(url, headers={'Content-Type': 'application/json'}, json=params)
            if response.status_code == 204:
                return 204
            elif response.status_code == 400:
                return 400
            else:
                print(f'ERROR: {response.status_code} - {response.text}')
                return None

        else:
            print(f'Error: missing session')
            return None

    def unlink_device_user(self, *, device_id, user_id):
        url = f"{self.__traccar_api_url}/api/permissions"
        params = {"userId": user_id, "deviceId": str(device_id)}
        if self.__traccar_api_session is not None:
            response = self.__traccar_api_session.delete(url, headers={'Content-Type': 'application/json'}, json=params)
            if response.status_code == 204:
                return 204
            elif response.status_code == 400:
                return 400
            else:
                print(f'ERROR: {response.status_code} - {response.text}')
                return None

        else:
            print(f'Error: missing session')
            return None

    def link_diver_device(self, *, driver_id, device_id):
        url = f"{self.__traccar_api_url}/api/permissions"
        params = {"deviceId": str(device_id), "driverId": driver_id}
        if self.__traccar_api_session is not None:
            response = self.__traccar_api_session.post(url, headers={'Content-Type': 'application/json'}, json=params)
            if response.status_code == 204:
                return 204
            elif response.status_code == 400:
                return 400
            else:
                print(f'ERROR: {response.status_code} - {response.text}')
                return None

        else:
            print(f'Error: missing session')
            return None

    def unlink_diver_device(self, *, driver_id, device_id):
        url = f"{self.__traccar_api_url}/api/permissions"
        params = {"deviceId": str(device_id), "driverId": driver_id}
        if self.__traccar_api_session is not None:
            response = self.__traccar_api_session.delete(url, headers={'Content-Type': 'application/json'}, json=params)
            if response.status_code == 204:
                return 204
            elif response.status_code == 400:
                return 400
            else:
                print(f'ERROR: {response.status_code} - {response.text}')
                return response.status_code

        else:
            print(f'Error: missing session')
            return None
