import requests


class AuthApi2:
    def __init__(self):
        self.session = requests.Session()

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
        self.session.get(endpoint, params=params)
        xsfr_token = self.session.cookies.items()
        return xsfr_token
