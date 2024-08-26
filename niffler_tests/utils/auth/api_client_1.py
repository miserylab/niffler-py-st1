import pkce
import requests
import os


class APIClient1:

    def __init__(self, user_name, user_password):
        self.code_verifier, self.code_challenge = pkce.generate_pkce_pair()
        self.user_name = user_name
        self.user_password = user_password
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        self.xsrf_token, self.jssessionid = self.init_session()

    def init_session(self):
        url = f'{os.getenv("AUTH_URL")}/login'

        data = {
            '_csrf': self.code_challenge,
            'username': self.user_name,
            'password': self.user_password
        }

        response = requests.post(url, headers=self.headers, data=data, allow_redirects=False)

        print(response.cookies)
        print(response.headers)
        print(response.url)
        print(response.status_code)
        print(f"'XSRF-TOKEN' : {response.cookies.get('XSRF-TOKEN')}")
        print(f"'JSESSIONID' : {response.cookies.get('JSESSIONID')}")

        return response.cookies.get('XSRF-TOKEN'), response.cookies.get('JSESSIONID')

    def init_authorization(self):
        url = f'{os.getenv("AUTH_URL")}/oauth2/authorize'

        params = {
            'response_type': 'code',
            'client_id': 'client',
            'scope': 'openid',
            'redirect_uri': f'{os.getenv("FRONTEND_URL")}/authorized',
            'code_challenge': self.code_challenge,
            'code_challenge_method': 'S256'
        }

        headers = self.headers
        headers['Cookie'] = f'JSESSIONID={self.jssessionid}; XSRF-TOKEN={self.xsrf_token}'

        response = requests.get(url, params=params, headers=headers, allow_redirects=False)

        print(response.cookies)
        print(response.headers)
        print(response.url)
        print(response.status_code)

    def get_code(self):
        self.init_authorization()
        url = f'{os.getenv("AUTH_URL")}/login'

        headers = self.headers
        headers['Cookie'] = f'JSESSIONID={self.jssessionid}; XSRF-TOKEN={self.xsrf_token}'
        data = {
            '_csrf': self.xsrf_token,
            'username': self.user_name,
            'password': self.user_password
        }

        response = requests.post(url, headers=headers, data=data, verify=False)  # , allow_redirects=False)

        print(response.cookies)
        print(response.headers)
        print(response.url)
        print(response.status_code)
        user_code = response.url[response.url.find("?code=") + len("?code="):]
        print(f"user_code : {user_code}")

        return user_code

    def get_tokens(self):
        url = f'{os.getenv("AUTH_URL")}/oauth2/token'

        data = {
            'code': self.get_code(),
            'redirect_uri': f'{os.getenv("FRONTEND_URL")}/authorized',
            'code_verifier': self.code_verifier,
            'grant_type': 'authorization_code',
            'client_id': 'client'
        }

        response = requests.post(url, data=data, headers=self.headers, verify=False, allow_redirects=False)

        print(response.cookies)
        print(response.headers)
        print(response.url)
        print(response.status_code)
        print(response.text)
        print(response.json())

        return response.json()["access_token"], response.json()["id_token"]

    def create_user(self):
        url = f'{os.getenv("AUTH_URL")}/register'

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': f'XSRF-TOKEN={self.code_challenge}',
            'Origin': os.getenv("AUTH_URL"),
            'Accept': 'application/json',
        }

        data = {
            '_csrf': self.code_challenge,
            'username': self.user_name,
            'password': self.user_password,
            'passwordSubmit': self.user_password
        }

        response = requests.post(url, headers=headers, data=data, verify=False, allow_redirects=False)

        print(response.cookies)
        print(response.headers)
        print(response.url)
        print(response.status_code)
        print(f"REGISTRED USER X-XSRF-TOKEN : {response.headers['X-XSRF-TOKEN']}")
        return response.headers['X-XSRF-TOKEN']
