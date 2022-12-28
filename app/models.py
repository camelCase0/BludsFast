from datetime import datetime
from enum import Enum

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float
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


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    password = Column(String, nullable=False)
    name = Column(String)
    blood_type = Column(String, default=Blood_type.Om.name)
    volume = Column(Float, default=0)
    status = Column(String, default=Status.D.name)
    created_at = Column(DateTime, default=datetime.utcnow())
    admin_id = Column(Integer, nullable=False)

    donations = relationship("Donations", back_populates="user")


class Donations(Base):
    __tablename__ = 'donations'

    record_id = Column(Integer, primary_key=True)
    volume = Column(Integer)
    date = Column(DateTime, default=datetime.utcnow())
    
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="donations")
    
    clinic_id = Column(Integer, ForeignKey('clinics.clinic_id'))
    clinic = relationship("Clinics", back_populates="donations")


class Clinics(Base):
    __tablename__ = 'clinics'

    clinic_id = Column(Integer, primary_key=True)
    address = Column(String)
    altitude = Column(Float)
    longitude = Column(Float)

    donations = relationship("Donations", back_populates="clinic")

#
# class AuthToken(Base):
#     __tablename__ = 'auth_token'
#
#     id = Column(Integer, primary_key=True)
#     token = Column(String)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     created_at = Column(String, default=datetime.utcnow())