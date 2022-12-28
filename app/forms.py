from datetime import datetime

from pydantic import BaseModel
# from typing import Optional
from .models import Status, Blood_type


class UserLoginForm(BaseModel):
    email: str
    password: str

class UserCreateForm(BaseModel):
    email: str
    password: str
    name: str
    blood_type: Blood_type
    status: Status

    class Config:
        orm_mode = True

class UserUpdateForm(BaseModel):
    email: str
    password: str
    name: str
    blood_type: Blood_type
    status: Status

    class Config:
        orm_mode = True

class DonationBase(BaseModel):
    volume: float
    date: datetime

    class Config:
        orm_mode = True

class UserGetForm(BaseModel):
    id: int
    email: str
    name: str
    blood_type: Blood_type
    volume: float
    status: Status
    donations: list[DonationBase]

    class Config:
        orm_mode = True

class UserGetAForm(BaseModel):
    id: int
    email: str
    name: str
    status: Status
    donors: list[UserGetForm]

    class Config:
        orm_mode = True


class DonationCreateForm(BaseModel):
    user_id: int
    volume: float


class DonationGetForm(BaseModel):
    name: str
    blood_type: Blood_type
    volume: float
    date: datetime

    class Config:
        orm_mode = True
