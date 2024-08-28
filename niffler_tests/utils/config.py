import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    app_url: str = os.getenv("APP_URL", default="")
    gateway_url: str = os.getenv("GATEWAY_URL", default="")
    auth_url: str = os.getenv("AUTH_URL", default="")

    username: str = os.getenv("AUTH_USERNAME", default="")
    password: str = os.getenv("AUTH_PASSWORD", default="")
