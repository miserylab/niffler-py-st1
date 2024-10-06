from datetime import datetime

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    username: str
    currency: str
    firstname: str
    surname: str
    photo: str
    photo_small: str


class Friendship(SQLModel, table=True):
    requester_id: str = Field(default=None, primary_key=True)
    addressee_id: str = Field(default=None, primary_key=True)
    status: str
    created_date: datetime
