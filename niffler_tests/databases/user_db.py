from typing import Sequence

from sqlalchemy import Engine, create_engine
from sqlmodel import Session, select

from niffler_tests.models.userdata import Friendship, User


class UserDb:
    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)

    def get_users(self) -> Sequence[User]:
        with Session(self.engine) as session:
            statement = select(User)
            return session.exec(statement).all()

    def get_user_by_username(self, username: str) -> User:
        with Session(self.engine) as session:
            statement = select(User).where(User.username == username)
            return session.exec(statement).one()

    def get_user_by_id(self, user_id: str) -> User:
        with Session(self.engine) as session:
            statement = select(User).where(User.id == user_id)
            return session.exec(statement).one()

    def delete_user_by_id(self, user_id: str) -> None:
        with Session(self.engine) as session:
            user = session.get(User, user_id)
            session.delete(user)
            session.commit()

    def get_friendship_by_requester_id(self, requester_id: str) -> Friendship:
        with Session(self.engine) as session:
            statement = select(Friendship).where(Friendship.requester_id == requester_id)
            return session.exec(statement).one()

    def get_friendship_by_addressee_id(self, addressee_id: str) -> Friendship:
        with Session(self.engine) as session:
            statement = select(Friendship).where(Friendship.addressee_id == addressee_id)
            return session.exec(statement).one()

    def delete_friendship(self, requester_id: str, addressee_id: str) -> None:
        with Session(self.engine) as session:
            friendship = session.get(Friendship, (requester_id, addressee_id))
            session.delete(friendship)
            session.commit()
