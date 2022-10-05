from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from .auth.auth_bearer import JWTBearer
from .auth.auth_handler import decodeJWT
from .models import User, Status, Blood_type
from .forms import UserCreateForm, UserUpdateForm
from .utils import get_password_hash


# USER CRUD
def create_user(database: Session, userform: UserCreateForm):
    new_user = User(
        email=userform.email,
        password=get_password_hash(userform.password),
        name=userform.name,
        blood_type=userform.blood_type.name,
        status=userform.status.name
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


def delete_user_by_id(database: Session, user_id: int):
    user_to_dell = database.query(User).filter(User.id == user_id)
    database.delete(user_to_dell)
    database.commit()
    return {'deleted user:': user_id}
