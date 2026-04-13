from sqlmodel import Session, select
from models.user import User,UserRole
from schemas.auth import SignupRequest, LoginRequest
from config.security import hash_password, verify_password, create_access_token


def create_user(session: Session, data: SignupRequest):
    existing_user = session.exec(
        select(User).where(User.email == data.email)
    ).first()

    if existing_user:
        raise ValueError("Email already registered")

    user = User(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
        role=UserRole.viewer
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def authenticate_user(session: Session, data: LoginRequest):
    user = session.exec(select(User).where(User.email == data.email)).first()

    if not user:
        return None

    if not verify_password(data.password, user.password):
        return None

    return user


def generate_token(user: User):
    token_data = {
        "sub":str(user.id),
        "role":user.role
    }

    return create_access_token(token_data)