from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from config.database import SessionDep
from schemas.auth import SignupRequest, LoginRequest, TokenResponse
from services.auth import create_user, authenticate_user, generate_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=TokenResponse)
def signup(data: SignupRequest, session: SessionDep):
    try:
        user = create_user(session, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    token = generate_token(user)
    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, session: SessionDep):
    user = authenticate_user(session, data)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is inactive")

    token = generate_token(user)
    return {
        "access_token": token,
        "token_type": "bearer"
    }