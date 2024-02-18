from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


class States(Base):
    __tablename__ = 'states'

    state_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    state_name = Column(String)


class Responsible(Base):
    __tablename__ = 'responsible'

    responsible_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    responsible_name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'))


class Clients(Base):
    __tablename__ = 'clients'

    client_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    client_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)


class Requests(Base):
    __tablename__ = 'requests'

    request_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    request_number = Column(Integer, unique=True, nullable=False)
    client_id = Column(Integer, ForeignKey('clients.client_id'))
    state_id = Column(Integer, ForeignKey('states.state_id'))
    responsible_id = Column(Integer, ForeignKey('responsible.responsible_id'))
    equipment = Column(Integer, nullable=False)
    type_of_fault = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
