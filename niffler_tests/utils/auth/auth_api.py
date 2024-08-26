import requests

from niffler_tests.utils.auth.api_client import ApiClient
from niffler_tests.utils.config import Config


class AuthApi:
    def __init__(self):
        self.client = ApiClient(base_url=Config.auth_url)

    def pre_request(self, response_type, client_id, scope, redirect_uri, code_challenge, code_challenge_method):
        endpoint = "oauth2/authorize"
        params = {
            "response_type": response_type,
            "client_id": client_id,
            "scope": scope,
            "redirect_uri": redirect_uri,
            "code_challenge": code_challenge,
            "code_challenge_method": code_challenge_method
        }
        # Send GET request to initiate the OAuth2 authorization
        self.client.get(endpoint, params=params)
        xsfr_token = self.client.session.cookies.items()
        return xsfr_token

    def login(self, csrf, username, password):
        url = "http://auth.niffler.dc:9000/login"  # Direct URL for login, bypassing the base_url
        data = {
            "_csrf": csrf,
            "username": username,
            "password": password
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # Send POST request for login with form data
        response = self.client.session.post(url, data=data, headers=headers, verify=False)

        # Check if the response indicates a successful login (usually by redirecting with a code)
        if response.status_code == 200 and "code=" in response.url:
            auth_code = response.url[response.url.find("?code=") + len("?code="):]
            print(f"Authorization Code: {auth_code}")
            return auth_code
        else:
            print(f"Login failed. Status code: {response.status_code}")
            print(f"Response content: {response.text}")
            raise ValueError("Login did not redirect to the expected URL with an authorization code")

    def token(self, code, redirect_uri, code_verifier, grant_type, client_id):
        endpoint = "oauth2/token"
        data = {
            "code": code,
            "redirect_uri": redirect_uri,
            "code_verifier": code_verifier,
            "grant_type": grant_type,
            "client_id": client_id
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = self.client.session.post(f"{self.client.base_url}/{endpoint}", data=data, headers=headers)
        return response.json()
