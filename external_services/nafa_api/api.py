import requests

from external_services.nafa_api.nafa_api_errors.nafa_api_errors import NafaApiAuthenticationError, NafaApiError


class NafaApi:
    def __init__(self, nafa_api_url: str, nafa_api_mail: str, nafa_api_pass: str):
        self.__nafa_api_url = nafa_api_url
        self.__nafa_api_mail = nafa_api_mail
        self.__nafa_api_pass = nafa_api_pass
        self.__nafa_api_session = None
        self.__nafa_api_session = requests.Session()
        self.__nafa_api_token = None

    def get_nafa_api_url(self):
        return self.__nafa_api_url

    def get_nafa_api_mail(self):
        return self.__nafa_api_mail

    def get_nafa_api_pass(self):
        return self.__nafa_api_pass

    def get_nafa_api_token(self):
        return self.__nafa_api_token

    def set_nafa_api_url(self, nafa_api_url: str) -> None:
        self.__nafa_api_url = nafa_api_url

    def set_nafa_api_mail(self, nafa_api_mail: str) -> None:
        self.__nafa_api_mail = nafa_api_mail

    def set_nafa_api_pass(self, nafa_api_pass: str) -> None:
        self.__nafa_api_pass = nafa_api_pass

    def set_nafa_api_token(self, token: str) -> None:
        self.__nafa_api_token = token

    def login(self):
        login_url = f"{self.__nafa_api_url}/api/auth/login"
        login_data = {
            'email': self.__nafa_api_mail,
            'password': self.__nafa_api_pass
        }
        try:
            response = self.__nafa_api_session.post(login_url, json=login_data, timeout=2)

            if response.status_code == 200:
                print('Login successful')
                # cookies = self.__nafa_api_session.cookies.get_dict()
                if response.json().get('token') is not None:
                    self.set_nafa_api_token(response.json().get('token'))
                return response.json()
            else:
                raise NafaApiAuthenticationError(
                    "Authentication failed",
                    status_code=response.status_code,
                    response_body=response.text,
                    details="Check username and password"
                )
        except requests.exceptions.RequestException as e:
            raise NafaApiError(f"Request failed: {str(e)}")

    def logout(self):
        if self.__nafa_api_session:
            self.__nafa_api_session.close()
            self.__nafa_api_session = None
            self.set_nafa_api_token(None)

    def get_vessel(self, *, cfr: str):
        headers = {'Authorization': 'Bearer ' + self.get_nafa_api_token(), 'Accept': 'application/json'}
        url = f"{self.__nafa_api_url}/api/ships/cfr/{cfr}"
        if self.__nafa_api_session:
            try:
                response = self.__nafa_api_session.get(url, headers=headers)
                response.raise_for_status()

                return response.json()

            except requests.exceptions.RequestException as e:
                raise NafaApiError(f"Failed to retrieve device: {str(e)}")

        else:
            raise NafaApiError("Error: Missing session for get_device.")

