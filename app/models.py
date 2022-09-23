from datetime import datetime
from enum import Enum

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Session, relationship

from app.config import DATABASE_URL

from .database import Base

class Blood_type(Enum):
    Op = "O(І) Rh(+)"
    Om = "O(І) Rh(-)"
    Ap = "O(ІI) Rh(+)"
    Am = "O(ІI) Rh(-)"
    Bp = "O(ІII) Rh(+)"
    Bm = "O(ІII) Rh(-)"
    ABp = "O(ІV) Rh(+)"
    ABm = "O(ІV) Rh(-)"


class Status(Enum):
    A = "Admin"
    D = "Donor"
    R = "Recepient"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String, nullable=False)
    name = Column(String)
    blood_type = Column(String, default=Blood_type.Om.value)
    status = Column(String, default=Status.D.value)
    created_at = Column(DateTime, default=datetime.utcnow())

    donations = relationship("Donations", back_populates="user")
    receives = relationship("Receives", back_populates="user")


class Donations(Base):
    __tablename__ = 'donations'

    record_id = Column(Integer, primary_key=True)
    volume = Column(Integer)
    date = Column(DateTime, default=datetime.utcnow())
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="donations")


class Receives(Base):
    __tablename__ = 'receives'

    record_id = Column(Integer, primary_key=True)
    volume = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'), nullable = False)

    user = relationship("User", back_populates="receives")
#
# class AuthToken(Base):
#     __tablename__ = 'auth_token'
#
#     id = Column(Integer, primary_key=True)
#     token = Column(String)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     created_at = Column(String, default=datetime.utcnow())