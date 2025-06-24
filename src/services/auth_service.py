from datetime import datetime, timedelta, UTC
import os

import bcrypt
from fastapi import HTTPException
from jose import jwt, JWTError
from psycopg.errors import UniqueViolation

from repositories.user_repository import create_user, get_user_by_username


REFRESH_TOKEN_SECRET = os.getenv('REFRESH_TOKEN_SECRET')
ALGORITHM = os.getenv('ALGORITHM')


ACCESS_SECRET = os.getenv("ACCESS_TOKEN_SECRET", "dev_secret")
REFRESH_SECRET = os.getenv("REFRESH_TOKEN_SECRET", "dev_refresh")
ACCESS_EXPIRES = int(os.getenv("ACCESS_TOKEN_EXPIRES", "3600"))       # 1 час по дефолту
REFRESH_EXPIRES = int(os.getenv("REFRESH_TOKEN_EXPIRES", "86400"))   # 24 часа по дефолту


def login(dto: dict) -> dict:
    user = get_user_by_username(dto["user_name"])
    if not user:
        raise ValueError("User not found")

    if not bcrypt.checkpw(dto["password"].encode(), user["password_hash"].encode()):
        raise ValueError("Wrong password")

    return generate_token_pair(user["id"])


def register(dto: dict) -> dict:
    password_hash = bcrypt.hashpw(dto["password"].encode(), bcrypt.gensalt()).decode()

    user_data = {
        "user_name": dto["user_name"],
        "password_hash": password_hash,
        "first_name": dto["first_name"],
        "last_name": dto["last_name"],
    }

    try:
        user = create_user(user_data)
    except UniqueViolation:
        raise ValueError("User already exists")
    return generate_token_pair(user["id"])


def generate_token_pair(user_id: int) -> dict:
    now = datetime.now(UTC)

    access_token = jwt.encode(
        {"sub": str(user_id), "exp": now + timedelta(seconds=ACCESS_EXPIRES)},
        ACCESS_SECRET,
        algorithm=ALGORITHM
    )

    refresh_token = jwt.encode(
        {"sub": str(user_id), "exp": now + timedelta(seconds=REFRESH_EXPIRES)},
        REFRESH_SECRET,
        algorithm=ALGORITHM
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


def refresh(token: str) -> dict:
    try:
        payload = jwt.decode(token, REFRESH_TOKEN_SECRET, algorithms=[ALGORITHM])
        return generate_token_pair(payload["sub"])
    except JWTError as e:
        raise HTTPException(status_code=401, detail=str(e))
