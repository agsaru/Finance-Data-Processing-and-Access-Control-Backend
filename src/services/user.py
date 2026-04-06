from sqlmodel import Session, select
from models.user import User
from schemas.user import UserCreate, UserUpdate
from config.security import hash_password

def get_all_users(session: Session):
    return session.exec(select(User)).all()

def get_user_by_id(session: Session, user_id: int):
    user = session.get(User, user_id)
    if not user:
        raise ValueError("User not found")
    return user

def create_user_admin(session: Session, data: UserCreate):
    existing_user = session.exec(select(User).where(User.email == data.email))

    if existing_user:
        raise ValueError("Email already exists")

    user = User(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
        role=data.role
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

def update_user(session: Session, user: User, data: UserUpdate):
    if data.name is not None:
        user.name = data.name

    if data.role is not None:
        user.role = data.role

    if data.status is not None:
        user.status = data.status

    if data.password is not None:
        user.password = hash_password(data.password)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def delete_user(session: Session, user: User):
    session.delete(user)
    session.commit()