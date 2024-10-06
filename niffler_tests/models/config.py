from pydantic import BaseModel


class Envs(BaseModel):
    app_url: str
    gateway_url: str
    auth_url: str
    spend_db_url: str
    user_db_url: str
    username: str
    password: str
