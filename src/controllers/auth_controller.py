from fastapi import APIRouter, HTTPException, Request, status

from dto.auth_dto import LoginDTO, RefreshDTO, RegisterDTO
from services.auth_service import login as login_service, register as register_service, refresh as refresh_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(dto: LoginDTO):
    try:
        tokens = login_service(dto.model_dump())
        return tokens
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/register", status_code=201)
def register(dto: RegisterDTO):
    try:
        tokens = register_service(dto.model_dump())
        return tokens
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/refresh")
def refresh(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    token = auth_header[7:]  # убираем "Bearer "

    try:
        tokens = refresh_service(token)
        return tokens
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
