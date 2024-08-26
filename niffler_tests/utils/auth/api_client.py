import json
import requests


class ApiClient:
    def __init__(self, base_url, api_key=None, follow_redirects=True):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.session()
        self.session.headers.update({
            "Content-Type": "application/json",
        })
        if api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {self.api_key}"
            })

        self.session.allow_redirects = follow_redirects

    def get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        response = self.session.get(url, params=params)
        return self._handle_response(response)

    def post(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        response = self.session.post(url, json=data)
        return self._handle_response(response)

    def put(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        response = self.session.put(url, json=data)
        return self._handle_response(response)

    def delete(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        response = self.session.delete(url)
        return self._handle_response(response)

    def _handle_response(self, response):
        print(f"Response status code: {response.status_code}")
        print(f"Response URL: {response.url}")
        print(f"Redirects: {response.history}")
        print(f"Response content: {response.text}")

        if 200 <= response.status_code < 300:
            if response.text.strip():  # Check if there's any content
                content_type = response.headers.get('Content-Type', '')
                if 'application/json' in content_type:
                    try:
                        return response.json()
                    except json.JSONDecodeError as e:
                        print(f"Failed to decode JSON: {e}")
                        raise
                elif 'text/html' in content_type:
                    print("Received HTML response.")
                    return response.text  # Handle or parse HTML as needed
                else:
                    print(f"Received unexpected content type: {content_type}")
                    return response.text  # Return raw text for unexpected content types
            else:
                raise ValueError("Empty response received where JSON was expected.")
        else:
            response.raise_for_status()
