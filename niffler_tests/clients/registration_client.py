from urllib.parse import urljoin

import pkce
import requests


class RegistrationHttpClient:
    session: requests.Session
    base_url: str

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.session()
        self.session.headers.update(
            {
                "Accept": "application/json",
            }
        )

    def register(self, username, password):
        code_verifier, code_challenge = pkce.generate_pkce_pair()
        headers = self.session.headers
        headers["Cookie"] = f"XSRF-TOKEN={code_challenge}"
        response = self.session.post(
            urljoin(self.base_url, "/register"),
            headers=headers,
            data={
                "_csrf": code_challenge,
                "username": str(username),
                "password": str(password),
                "passwordSubmit": str(password),
            },
        )

        self.raise_for_status(response)
        return response.headers["X-XSRF-TOKEN"]

    @staticmethod
    def raise_for_status(response: requests.Response):
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            if response.status_code == 400:
                e.add_note(response.text)
                raise
