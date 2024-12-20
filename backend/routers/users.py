from fastapi import APIRouter, Request, Body, Query, Depends, status, Response
from fastapi.responses import JSONResponse
from database.models.user import User
from typing import Annotated
from passlib.context import CryptContext
from pydantic import BaseModel
from database.models.base import session
from datetime import datetime
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


async def is_user_authenticated(request: Request):
    return request.session.get("user_session_id")


async def authenticate_user(user: UserLogin):
    user_instance = User.query.filter(User.username == user.username).value(
        User.password
    )
    if not user_instance:
        return False

    # Verifying the password
    plain_password = user.password
    hashed_password = user_instance
    return verify_password(plain_password, hashed_password)


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

    if User.query.filter(User.username == user.username).value(User.email):
        return JSONResponse(
            {"error": "Username Exist!"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if User.query.filter(User.email == user.email).value(User.email):
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
    request: Request,
    is_authenticated: bool = Depends(is_user_authenticated),
    authenticate_user: bool = Depends(authenticate_user),
):
    print(request.session.get('user_session_id'))
    if is_authenticated:
        return JSONResponse(
            {"error": "User is already logged in!"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if not authenticate_user:
        return JSONResponse(
            {"error": "Eaither username or password is wrong!"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    random_session_id = random.randint(100000, 999999)
    request.session["user_session_id"] = random_session_id

    return JSONResponse(
        {"message": request.session['user_session_id']},
        status_code=status.HTTP_200_OK,
    )
