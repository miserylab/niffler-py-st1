from niffler_tests.utils.config import Config


class Urls:
    def __init__(self, url=None):
        self._url = url or Config.app_url
        self._auth_url = Config.auth_url

    path_api: dict[str, str] = {
        "users": "/api/users/",
    }

    def api_url(self, type_url: str) -> str:
        return f"{self._url}{self.path_api[type_url]}"

    def auth_url(self) -> str:
        return f"{self._auth_url}:9000/oauth2/token"
