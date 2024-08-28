from urllib.parse import urljoin

import requests


class CategoryHttpClient:
    session: requests.Session
    base_url: str

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.session = requests.session()
        self.session.headers.update(
            {"Accept": "application/json", "Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        )

    def get_categories(self):
        response = self.session.get(urljoin(self.base_url, "/api/categories/all"))
        response.raise_for_status()
        return response.json()

    def add_category(self, name: str):
        response = self.session.post(urljoin(self.base_url, "/api/categories/add"), json={"category": name})
        response.raise_for_status()
        return response.json()
