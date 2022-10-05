import uuid
from datetime import date, datetime
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette import status

from app.forms import UserLoginForm, UserCreateForm, UserGetForm, DonationCreateForm, DonationGetForm
from app.models import User, Status, Donations, Blood_type, Base
from app.utils import get_password_hash
# from app.auth import check_auth_token

from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT, decodeJWT
from .database import SessionLocal, engine
from . import crud
Base.metadata.create_all(bind=engine)

router = APIRouter()

# @router.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
# def add_post(post: PostSchema):
#     post.id = len(posts) + 1
#     posts.append(post.dict())
#     return {
#         "data": "post added."
#     }
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", tags=["user"], name='user:create')#dependencies=[Depends(JWTBearer())],
def create_user(userform: UserCreateForm = Body(...), database: Session = Depends(get_db), token=Depends(JWTBearer())):
    # loged_user = get_curent_user(database, token)
    user_id = decodeJWT(token)['user_id']
    loged_user = database.query(User).filter(User.id == user_id).one_or_none()

    if not loged_user.status == Status.A.name:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin is permited!")

    exists_user = database.query(User.id).filter(User.email == userform.email).one_or_none()
    if exists_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    new_user = User(
        email=userform.email,
        password=get_password_hash(userform.password),
        name=userform.name,
        blood_type=userform.blood_type.name,
        status=userform.status.name
    )

    database.add(new_user)
    database.commit()

    return status.HTTP_201_CREATED


@router.post("/login", tags=["user"])
def user_login(user_form: UserLoginForm = Body(...), database=Depends(get_db)):
    user = database.query(User).filter(User.email == user_form.email).one_or_none()
    if not user or get_password_hash(user_form.password) != user.password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email/password is incorect")
    return signJWT(user.id)


@router.get('/user/{user_id}', tags=["user"], response_model=UserGetForm, dependencies=[Depends(JWTBearer())], name='user:get')
def get_user(user_id: int, database=Depends(get_db)):
    user = database.query(User).filter(User.id == user_id).one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such user")
    user.status = Status[user.status]
    user.blood_type = Blood_type[user.blood_type]
    return user

@router.get('/user', tags=["user"], response_model=UserGetForm, dependencies=[Depends(JWTBearer())], name='curent_user:get')
def get_curent_user(database=Depends(get_db), token=Depends(JWTBearer())):
    user_id = decodeJWT(token)['user_id']
    user = database.query(User).filter(User.id == user_id).one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such user")
    print(user.status)
    user.status = Status[user.status]
    print(user.status)
    user.blood_type = Blood_type[user.blood_type]
    return user


@router.get('/users', tags=["user"], response_model=List[UserGetForm], name='user:get_all')#, dependencies=[Depends(JWTBearer())]
def get_all_user(database=Depends(get_db)):
    users = crud.get_all_users(database)
    for user in users:
        user.status = Status[user.status]
        user.blood_type = Blood_type[user.blood_type]
    return users


# D  O  N  A  T  I  O  N  S
@router.get('/donations', tags=["donations"], response_model=List[DonationGetForm],  name='donate:get all')# dependencies=[Depends(JWTBearer())],
def get_all_donation(database=Depends(get_db)):

    dons = database.query(Donations).order_by(Donations.date.desc()).all()
    if not dons:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    for don in dons:
        user = get_user(don.user_id, database)
        don.name = user.name
        don.blood_type = user.blood_type.value
    return dons

@router.post('/donations', tags=["donations"],  name='donate:create') #dependencies=[Depends(JWTBearer())],
def create_donation(donate_form: DonationCreateForm = Body(...), database=Depends(get_db)):
    # btype = Blood_type[str(donate_form.blood_type)]
    record = database.query(Donations).filter(Donations.user_id == donate_form.user_id).order_by(Donations.date.desc()).first()
    cur_date = datetime.now()
    if record:
        next_time = datetime(year=record.date.year, month=record.date.month+2, day=record.date.day, hour=record.date.hour, minute=record.date.minute)

        if (next_time>cur_date):
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Donor has donated resently. Donate_after {next_time}")

    new_record = Donations(
        user_id=donate_form.user_id,
        volume=donate_form.volume,
    )
    database.add(new_record)
    database.commit()
    return {'created_record':new_record.date, 'user_id':new_record.user_id}