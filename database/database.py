from typing import Type

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base, Users, Requests

url = 'postgresql+psycopg2://postgres:1234@localhost:5432/pr02'


class BaseDatabase:
    def __init__(self) -> None:
        engine = create_engine(url)
        Base.metadata.create_all(engine)
        Session = sessionmaker(engine)
        self.session = Session()


class UserDatabase(BaseDatabase):
    def insert_user(self, user: Users) -> bool:
        if user.username is None:
            return False
        elif user.password is None:
            return False

        self.session.add(user)
        self.session.commit()

    def filter_user(self, **value) -> list[Type[Users]]:
        return self.session.query(Users).filter_by(**value).all()


class RequestDatabase(BaseDatabase):
    def get_all_requests(self) -> list[Type[Requests]]:
        return self.session.query(Requests).all()

    def get_request_by_id(self, request_id) -> Type[Requests]:
        ...

    def update_request_state(self, request_id, state) -> bool:
        ...
