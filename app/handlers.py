import uuid
from datetime import date, datetime
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette import status

from app.forms import UserLoginForm, UserCreateForm, UserGetForm, DonationCreateForm, DonationGetForm, ClinicCreateForm, ClinicGetForm
from app.models import User, Status, Donations, Blood_type, Base, Clinics
from app.utils import get_password_hash
# from app.auth import check_auth_token

from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT, decodeJWT
from .database import SessionLocal, engine
from . import crud
Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", tags=["temp"])
def index():
    return 200

@router.post("/register", tags=["user"], name='user:create', status_code=201)#dependencies=[Depends(JWTBearer())],
def create_user(userform: UserCreateForm = Body(...), database: Session = Depends(get_db), token=Depends(JWTBearer())):
    loged_user = crud.get_user_by_token(database, token)
   
    if not loged_user.status == Status.A.name:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin is permited!")

    exists_user = database.query(User.id).filter(User.email == userform.email).one_or_none()
    if exists_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    crud.create_user(database, userform, loged_user.id)
    
    return status.HTTP_201_CREATED


@router.post("/login", tags=["user"])
def user_login(user_form: UserLoginForm = Body(...), database=Depends(get_db)):

    user = database.query(User).filter(User.email == user_form.email).one_or_none()
    if not user or get_password_hash(user_form.password) != user.password:
        #DEBUGG
        if user_form.email == "a":         #REMOVE IN PROD
            crud.create_admin(database)    #REMOVE IN PROD
            return status.HTTP_201_CREATED #REMOVE IN PROD

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email/password is incorect")
    return signJWT(user.id)

@router.get('/users', tags=["user"], response_model=List[UserGetForm],dependencies=[Depends(JWTBearer())], name='user:get_all')#, dependencies=[Depends(JWTBearer())]
def get_all_user(database=Depends(get_db)):
    users = crud.get_all_users(database)
    for user in users:
        user.status = Status[user.status]
        user.blood_type = Blood_type[user.blood_type]
    return users

@router.get('/user', tags=["user"], response_model=UserGetForm, dependencies=[Depends(JWTBearer())], name='curent_user:get')
def get_curent_user(database=Depends(get_db), token=Depends(JWTBearer())):
    user = crud.get_user_by_token(database, token)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such user")

    user.status = Status[user.status].value
    user.blood_type = Blood_type[user.blood_type].value
    return user

@router.get('/user/{user_id}', tags=["user"], response_model=UserGetForm, name='user:get')
def get_user(user_id: int, database=Depends(get_db), token=Depends(JWTBearer())):

    loged_user = crud.get_user_by_token(database, token) 
    if not loged_user.status == Status.A.name:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin is permited!")

    user = crud.get_user_by_id(database, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No such user")
    user.status = Status[user.status]
    user.blood_type = Blood_type[user.blood_type]
    return user

@router.delete('/user/{user_id}', tags=["user"], name='user:delete by id', status_code=200)
def delete_user(user_id: int, database=Depends(get_db), token=Depends(JWTBearer())):
    loged_user = crud.get_user_by_token(database, token)
    if not loged_user.status == Status.A.name:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin is permited!")
    
    user = crud.get_user_by_id(database, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such user")

    return crud.delete_user_by_id(database, user_id)
     

# D  O  N  A  T  I  O  N  S
@router.get('/donations', tags=["donations"], response_model=List[DonationGetForm],dependencies=[Depends(JWTBearer())], name='donate:get all')# dependencies=[Depends(JWTBearer())],
def get_all_donation(database=Depends(get_db)):

    dons = database.query(Donations).order_by(Donations.date.desc()).all()
    if not dons:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    for don in dons:
        don.user.blood_type = Blood_type[don.user.blood_type]
    return dons

@router.post('/donations', tags=["donations"], status_code=201, dependencies=[Depends(JWTBearer())], name='donate:create') #dependencies=[Depends(JWTBearer())],
def create_donation(donate_form: DonationCreateForm = Body(...), database=Depends(get_db)):
    
    record = database.query(Donations).filter(Donations.user_id == donate_form.user_id).order_by(Donations.date.desc()).first()
    cur_date = datetime.now()

    if record:
        next_time = datetime(year=record.date.year + int(record.date.month / 12), month=(record.date.month+2)%12, day=record.date.day, hour=record.date.hour, minute=record.date.minute)
        if (next_time>cur_date):
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Donor has donated resently. Donate_after {next_time}")
    # CHECK ON INPUT DONATE_FORM DATA
    if not crud.get_user_by_id(database, donate_form.user_id) or not crud.get_clinic_by_id(database, donate_form.clinic_id): 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Wrong Body')
        
    new_record = Donations(
        user_id=donate_form.user_id,
        volume=donate_form.volume,
        clinic_id=donate_form.clinic_id
    )
    database.add(new_record)
    database.commit()

    crud.update_user_volume(database, donate_form.volume, donate_form.user_id)
    
    return {'created_record':new_record.date, 'user_id':new_record.user_id}


# C L I N I C -------------------------------------------------------------------------------------------------
@router.post('/clinic',tags=['clinic'], status_code=201, name="clinic:create")
def create_clinic(clinic_form: ClinicCreateForm = Body(...), database=Depends(get_db), token=Depends(JWTBearer())):
    loged_user = crud.get_user_by_token(database, token)
    if not loged_user.status == Status.A.name:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin is permited!")

    clinic = database.query(Clinics).filter(Clinics.address == clinic_form.address).one_or_none()
    if clinic:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Address already registered")
    crud.create_clinic(database, clinic_form)
    return status.HTTP_201_CREATED

@router.delete('/clinic/{cl_id}',tags=['clinic'],status_code=200, name="clinic:delete")
def delete_clinic(cl_id:int, database=Depends(get_db), token=Depends(JWTBearer())):
    loged_user = crud.get_user_by_token(database, token)
    if not loged_user.status == Status.A.name:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin is permited!")

    clinic = crud.get_clinic_by_id(database, cl_id)
    if not clinic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No clinics with such id")
    crud.delete_clinic(database, cl_id)
    return clinic

@router.get('/clinics', tags=['clinic'], response_model=List[ClinicGetForm], name="clinic:get all")
def get_all_clinic(database=Depends(get_db)):
    clinics = database.query(Clinics).all()
    if not clinics:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No clinics in DB")
    return clinics


@router.get('/clinic/{cl_id}', tags=['clinic'], response_model=ClinicGetForm, name="clinic:get by id")
def get_clinic(cl_id:int, database=Depends(get_db)):
    clinic = crud.get_clinic_by_id(database, cl_id)
    if not clinic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No clinics with such id")
    return clinic
