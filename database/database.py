from typing import Type

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base, Users

url = 'postgresql+psycopg2://postgres:1234@localhost:5432/pr02'


class BaseDatabase:
    def __init__(self) -> None:
        engine = create_engine(url)
        Base.metadata.create_all(engine)
        Session = sessionmaker(engine)
        self.session = Session()


class UserDatabase(BaseDatabase):
    def insert_user(self, user: 'Users') -> bool:
        ...

    def filter_user(self, **value) -> list[Type['Users']]:
        ...
