from datetime import datetime

from pydantic import BaseModel
# from typing import Optional
from .models import Status, Blood_type

# USER
class UserLoginForm(BaseModel):
    email: str
    password: str

class UserBase(BaseModel):
    id: int
    email: str
    name: str
    blood_type: Blood_type

    class Config:
        orm_mode = True

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
    admin_id: int
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
    clinic_id: int

class ClinicBase(BaseModel):
    clinic_id: int
    address: str
    altitude: float
    longitude: float

    class Config:
        orm_mode = True

class DonationGetForm(BaseModel):
    record_id: int
    user: UserBase
    volume: float
    clinic: ClinicBase
    date: datetime
    
    class Config:
        orm_mode = True

class DonationBaseClinic(BaseModel):
    user_id: int
    volume: float
    date: datetime

    class Config:
        orm_mode = True

class ClinicGetForm(ClinicBase):
    donations: list[DonationBaseClinic]

    class Config:
        orm_mode = True

class ClinicCreateForm(BaseModel):
    address: str
    altitude: float
    longitude: float

