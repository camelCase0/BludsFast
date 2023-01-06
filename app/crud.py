from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from .auth.auth_bearer import JWTBearer
from .auth.auth_handler import decodeJWT
from .models import User, Status, Blood_type, Clinics
from .forms import UserCreateForm, UserUpdateForm, ClinicCreateForm
from .utils import get_password_hash


# USER CRUD -------------------------------------------------------
def create_user(database: Session, userform: UserCreateForm, adm_id):
    new_user = User(
        email=userform.email,
        password=get_password_hash(userform.password),
        name=userform.name,
        blood_type=userform.blood_type.name,
        status=userform.status.name,
        admin_id=adm_id
    )
    database.add(new_user)
    database.commit()
    database.refresh(new_user)
    return new_user

def create_admin(database: Session):
    new_user = User(
        email="a",
        password=get_password_hash(1),
        name="Admin",
        status=Status.A.name,
        admin_id="1"
    )
    database.add(new_user)
    database.commit()
    database.refresh(new_user)
    return new_user


def get_user_by_token(database: Session, token: JWTBearer()):
    user_id = decodeJWT(token)['user_id']
    return database.query(User).filter(User.id == user_id).one_or_none()


def get_user_by_id(database: Session, user_id: int):
    return database.query(User).filter(User.id == user_id).one_or_none()

def get_all_users(database: Session):
    return database.query(User).all()

def update_user(database: Session, userform: UserUpdateForm, user_id: int):
    old_user = database.query(User).filter(User.id == user_id)

    old_user.update({
        'email': userform.email,
        'name': userform.name,
        'status': userform.status,
        'blood_type': userform.blood_type,
        'password': userform.password
    })
    database.commit()
    return userform

def update_user_volume(database: Session, don_volume: int, user_id: int):
    old_user = database.query(User).filter(User.id == user_id)
    volume = database.query(User).filter(User.id == user_id).one_or_none().volume + don_volume
    old_user.update({
        'volume': volume,
    })
    database.commit()
    return {"new volume is ": volume}


def delete_user_by_id(database: Session, user_id: int):
    user_to_dell = get_user_by_id(database, user_id)
    database.delete(user_to_dell)
    database.commit()
    return {'deleted user:': user_id}

# C L I N I C --------------------------------------------
def create_clinic(database: Session, cform:ClinicCreateForm):
    new_clinic = Clinics(
        address= cform.address,
        altitude= cform.altitude,
        longitude= cform.longitude
    )
    database.add(new_clinic)
    database.commit()
    database.refresh(new_clinic)
    return new_clinic

def get_clinic_by_id(database: Session, id: int):
    return database.query(Clinics).filter(Clinics.clinic_id == id).one_or_none()

def delete_clinic(database: Session, id: int):
    clinic = get_clinic_by_id(database, id)
    database.delete(clinic)
    database.commit()
    return{'deleted_clinic': id}
    
