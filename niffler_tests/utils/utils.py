import base64
import datetime
import hashlib
import os
from urllib.parse import parse_qs, urlparse


class Utils:
    @staticmethod
    def get_timestamp() -> int:
        return int(datetime.datetime.utcnow().timestamp())

    @staticmethod
    def generate_code_verifier():
        """Generates a high-entropy cryptographic random string for the code verifier."""
        return base64.urlsafe_b64encode(os.urandom(32)).rstrip(b"=").decode("utf-8")

    @staticmethod
    def generate_code_challenge(code_verifier):
        """Generates the code challenge based on the code verifier."""
        code_challenge_digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()
        return base64.urlsafe_b64encode(code_challenge_digest).rstrip(b"=").decode("utf-8")

    @staticmethod
    def generate_code():
        token = os.urandom(32)
        return base64.urlsafe_b64encode(token).decode("utf-8")

    @staticmethod
    def extract_code_from_url(url):
        parsed_url = urlparse(url)
        code = parse_qs(parsed_url.query).get("code", [None])[0]
        return code
