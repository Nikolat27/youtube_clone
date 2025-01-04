from fastapi import APIRouter, Body, Query, status
from fastapi.responses import JSONResponse
from database.models.user import User, UserLogInfo, Channel
from passlib.context import CryptContext
from pydantic import BaseModel
from database.models.base import session
from datetime import datetime, timedelta
import random

router = APIRouter(prefix="/users", tags=["users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Base Models for serialization
class UserRegister(BaseModel):
    username: str
    email: str
    password1: str
    password2: str


class UserLogin(BaseModel):
    username: str
    password: str


# Hashing
def hash_password(plain_password):
    return pwd_context.hash(plain_password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def is_user_authenticated(user_session_id):
    if not user_session_id:
        return False  # User has to authenticate because he doesnt have any session

    user_login_date = (
        UserLogInfo.query.with_entities(UserLogInfo.user_id, UserLogInfo.created_at)
        .filter_by(session_id=user_session_id)
        .first()
    )
    if not user_login_date:
        return False  # User has to authenticate because he doesn`t have any active records in the DB

    expiration_time = user_login_date.created_at + timedelta(days=2)
    if datetime.now() < expiration_time:
        return True  # Everything is ok and user doesnt have to authenticate (his session is not expired yet)

    user_login_instance = (
        UserLogInfo.query.filter_by(  # Deleting the instance because its expired
            session_id=user_session_id
        ).first()
    )
    session.delete(user_login_instance)
    session.commit()
    return False  # User has to authenticate again because his session was expired


@router.get("/is_authenticated")
async def user_authentication_situation(  # This function is just used to return the user`s situation to frontend
    user_session_id: str = Query(None),
):
    return await is_user_authenticated(user_session_id)


async def authenticate_user(user: UserLogin):
    user_instance = (
        User.query.with_entities(User.id, User.password)
        .filter_by(username=user.username)
        .first()
    )
    if not (user_instance and verify_password(user.password, user_instance.password)):
        return None  # If credentials werent valid!
    return user_instance


@router.get("/")
async def all_users():
    users = User.query.all()
    return list(users)


@router.post("/register")
async def register_user(user: UserRegister):
    if user.password1 != user.password2:
        return JSONResponse(
            {"error": "Passwords aren`t matched!"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if User.query.filter_by(username=user.username).first():
        return JSONResponse(
            {"error": "Username Exist!"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if User.query.filter_by(email=user.email).first():
        return JSONResponse(
            {"error": "Email Exist!"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    hashed_password = hash_password(user.password1)
    user_instance = User(
        username=user.username, email=user.email, password=hashed_password
    )

    session.add(user_instance)
    session.commit()

    return JSONResponse(
        {"message": "User created successfully!"}, status_code=status.HTTP_200_OK
    )


@router.post("/login")
async def login_user(
    user_session_id: str = Query(None),
    user: UserLogin = Body(),
):
    user_instance = await authenticate_user(user)
    if not user_instance:
        return JSONResponse({"error": "Either your username or password is wrong!"})

    generate_new_session_id = random.randint(100000, 999999)

    if user_session_id:  # If user is already logged in
        is_authenticated = await is_user_authenticated(user_session_id)
        if is_authenticated:
            return JSONResponse(
                {"error": "User is already logged in!"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        else:
            user_login_instance = UserLogInfo.query.filter(
                UserLogInfo.user_id == user_instance.id
            ).first()
            if user_login_instance:
                user_login_instance.session_id = str(generate_new_session_id)
            else:
                return JSONResponse({"error": "No record found for the user!"})
    else:  # User is not logged in yet
        user_login_instance = UserLogInfo.query.filter(
            UserLogInfo.user_id == user_instance.id
        ).first()
        if user_login_instance:
            user_login_instance.session_id = str(generate_new_session_id)
        else:
            new_user_log_instance = UserLogInfo(
                user_id=user_instance.id, session_id=str(generate_new_session_id)
            )
            session.add(new_user_log_instance)

    print(generate_new_session_id)
    session.commit()
    return JSONResponse(
        {"user_session_id": generate_new_session_id}, status_code=status.HTTP_200_OK
    )


@router.get("/logout")
async def logout(user_session_id: str = Query()):
    is_authenticated = await is_user_authenticated(user_session_id)
    if not is_authenticated:
        return JSONResponse(
            {"error": "User is already logged out !"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    user = UserLogInfo.query.filter_by(session_id=user_session_id).first()
    session.delete(user)
    session.commit()

    return JSONResponse(
        {"data": "User logged out successfully!"},
        status_code=status.HTTP_200_OK,
    )


@router.get("/profile-picture")
async def get_user_profile(user_session_id: str = Query()):
    user = (
        UserLogInfo.query.with_entities(UserLogInfo.user_id)
        .filter_by(session_id=user_session_id)
        .first()
    )

    channel = (
        Channel.query.with_entities(Channel.profile_picture_url)
        .filter_by(owner_id=user.user_id)
        .first()
    )
    profile_picture = f"http://127.0.0.1:8000/static/{channel.profile_picture_url}"
    return JSONResponse(
        {"profile_picture": profile_picture or "", "user_id": user.user_id},
        status_code=status.HTTP_200_OK,
    )
