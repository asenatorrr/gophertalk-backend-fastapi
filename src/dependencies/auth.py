from fastapi import Depends, HTTPException, Request
from jose import jwt, JWTError
from pydantic import BaseModel
from os import getenv

ACCESS_TOKEN_SECRET = getenv("ACCESS_TOKEN_SECRET")
ALGORITHM = getenv("ALGORITHM")


class TokenPayload(BaseModel):
    sub: int  # ID пользователя
    exp: int  # время жизни токена


def get_current_user(request: Request) -> TokenPayload:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    token = auth_header[7:]  # убираем "Bearer "

    try:
        payload = jwt.decode(token, ACCESS_TOKEN_SECRET, algorithms=[ALGORITHM])
        user = TokenPayload(**payload)
        request.state.user = user
        return user
    except JWTError as e:
        raise HTTPException(status_code=401, detail=str(e))


def verify_same_user(user_id: int, token: TokenPayload = Depends(get_current_user)):
    if token.sub != int(user_id):
        raise HTTPException(status_code=401, detail="Forbidden")
    return token
