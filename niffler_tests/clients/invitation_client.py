from http import HTTPStatus
from urllib.parse import urljoin

import requests


class InvitationHttpClient:
    session: requests.Session
    base_url: str

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
        )

    def get_income_invitations(self):
        response = self.session.get(urljoin(self.base_url, "/api/invitations/income"))
        self.raise_for_status(response)
        return response.json()

    def get_outcome_invitations(self):
        response = self.session.get(urljoin(self.base_url, "/api/invitations/outcome"))
        self.raise_for_status(response)
        return response.json()

    def send_invitation(self, body):
        response = self.session.post(urljoin(self.base_url, "/api/invitations/send"), json=body)
        self.raise_for_status(response)
        assert response.status_code == HTTPStatus.OK
        return response.json()

    def accept_invitation(self, body):
        response = self.session.post(urljoin(self.base_url, "/api/invitations/accept"), json=body)
        self.raise_for_status(response)
        return response.json()

    def decline_invitation(self, body):
        response = self.session.post(urljoin(self.base_url, "/api/invitations/decline"), json=body)
        self.raise_for_status(response)
        return response.json()

    @staticmethod
    def raise_for_status(response: requests.Response):
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            if response.status_code == 400:
                e.add_note(response.text)
                raise
