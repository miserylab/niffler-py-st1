import requests
import threading
from playwright.sync_api import sync_playwright

class ApiLoginExtension:
    _context = threading.local()

    def __init__(self, base_url, init_browser=True):
        self.base_url = base_url
        self.session = requests.Session()
        self.init_browser = init_browser
        self.browser = None
        self.page = None

    @staticmethod
    def set_value(key, value):
        setattr(ApiLoginExtension._context, key, value)

    @staticmethod
    def get_value(key):
        return getattr(ApiLoginExtension._context, key, None)

    def before_each(self, username, password):
        code_verifier = self.generate_code_verifier()
        code_challenge = self.generate_code_challenge(code_verifier)
        self.set_value('code_verifier', code_verifier)
        self.set_value('code_challenge', code_challenge)

        self.do_login(username, password)

        if self.init_browser:
            self.start_browser()
            self.setup_session_storage()
            self.page.reload()

    def after_each(self):
        self.clear_cookies()
        if self.browser:
            self.browser.close()

    def start_browser(self):
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(headless=False)  # Change to headless=False if you need to see the browser
        self.page = self.browser.new_page()
        self.page.goto(self.base_url)

        # Add the JSESSIONID cookie
        self.page.context.add_cookies([{
            'name': 'JSESSIONID',
            'value': self.session.cookies.get("JSESSIONID"),
            'url': self.base_url
        }])

    def setup_session_storage(self):
        self.page.evaluate(f"sessionStorage.setItem('codeChallenge', '{self.get_value('code_challenge')}');")
        self.page.evaluate(f"sessionStorage.setItem('id_token', '{self.get_value('token')}');")
        self.page.evaluate(f"sessionStorage.setItem('codeVerifier', '{self.get_value('code_verifier')}');")

    def do_login(self, username, password):
        # Simulate OAuth2 flow for logging in
        auth_url = f"{self.base_url}/oauth2/authorize"
        auth_params = {
            "response_type": "code",
            "client_id": "client",
            "scope": "openid",
            "redirect_uri": f"{self.base_url}/authorized",
            "code_challenge": self.get_value('code_challenge'),
            "code_challenge_method": "S256"
        }
        self.session.get(auth_url, params=auth_params)

        csrf_token = self.session.cookies.get("XSRF-TOKEN")
        login_url = f"{self.base_url}/login"
        login_data = {
            "_csrf": csrf_token,
            "username": username,
            "password": password
        }
        self.session.post(login_url, data=login_data)

        token_url = f"{self.base_url}/oauth2/token"
        token_data = {
            "code": self.get_value('code'),
            "redirect_uri": f"{self.base_url}/authorized",
            "code_verifier": self.get_value('code_verifier'),
            "grant_type": "authorization_code",
            "client_id": "client"
        }
        response = self.session.post(token_url, data=token_data)
        response.raise_for_status()
        token_response = response.json()
        self.set_value('token', token_response['id_token'])

    def clear_cookies(self):
        self.session.cookies.clear()

    # @staticmethod
    # def generate_code_verifier():
    #     # Return a fixed code verifier for simplicity
    #     return "some_code_verifier"
    #
    # @staticmethod
    # def generate_code_challenge(code_verifier):
    #     # Return a fixed code challenge for simplicity
    #     return "some_code_challenge"