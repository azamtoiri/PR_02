from typing import Type

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base, Users, Requests, Responsible, Clients, States

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
    def get_states(self) -> list[Type[States]]:
        return self.session.query(States).all()
    def get_state_id(self, state) -> Type[States]:
        return self.session.query(States).where(States.state_name == state).first()

    def get_state_by_id(self, _id) -> Type[States]:
        return self.session.query(States).filter(States.state_id == _id).first()

    def get_all_requests(self) -> list[Type[Requests]]:
        return self.session.query(Requests).all()

    def get_request_by_id(self, request_id) -> Type[Requests]:
        return self.session.query(Requests).filter(Requests.request_id == request_id).first()

    def add_request(self, req: Requests) -> bool:
        try:
            self.session.add(req)
            self.session.commit()
            return True
        except Exception as ex:
            print(ex)
            return False

    def update_request_state(self, request_id, state) -> bool:
        ...

    def update_description(self, _id, description: str) -> bool:
        try:
            req = self.get_request_by_id(_id)
            req.description = description
            self.session.commit()
            return True
        except Exception as ex:
            print(ex)
            return False

    def get_request_by_request_number(self, req_number) -> Type[Requests]:
        return self.session.query(Requests).filter(Requests.request_number == req_number).first()

    def get_request_by_type_of_fault(self, type_of_fault) -> list[Type[Requests]]:
        return self.session.query(Requests).where(Requests.type_of_fault.ilike(f"%{type_of_fault}%")).all()

    def get_responsible(self) -> list[Type[Responsible]]:
        return self.session.query(Responsible).all()

    def get_responsible_by_id(self, _id) -> Type[Responsible]:
        return self.session.query(Responsible).filter(Responsible.responsible_id == _id).first()

    def get_responsible_by_name(self, fio) -> Type[Responsible]:
        return self.session.query(Responsible).filter(Responsible.responsible_name == fio).first()

    def get_client_by_id(self, client_id) -> Type[Clients]:
        return self.session.query(Clients).filter(Clients.client_id == client_id).first()

    def add_client(self, client_name: str, phone: str) -> bool | Type[Clients]:
        try:
            _client = Clients(client_name=client_name, phone_number=phone)
            self.session.add(_client)
            self.session.commit()
            return _client
        except Exception as ex:
            print(ex)
            return False

    def get_client_by_fio(self, fio: str) -> list[Type[Clients]]:
        return self.session.query(Clients).where(Clients.client_name.ilike(f'%{fio}%')).all()

    def get_all_clients(self) -> list[Type[Clients]]:
        return self.session.query(Clients).all()

