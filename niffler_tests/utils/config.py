import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    username: str = os.getenv("AUTH_USERNAME", default="")
    password: str = os.getenv("AUTH_PASSWORD", default="")
