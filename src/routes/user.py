from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from config.database import SessionDep
from config.security import require_roles, get_current_user
from schemas.user import UserCreate, UserRead, UserUpdate
from models.user import UserRole
from services.user import (
    get_all_users,
    get_user_by_id,
    create_user_admin,
    update_user,
    delete_user
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserRead])
def get_users(session: SessionDep,user = Depends(require_roles([UserRole.admin]))):
    return get_all_users(session)

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int,session: SessionDep,current_user = Depends(get_current_user)):
    if current_user.id != user_id and current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not authorized to view this user")
    user = get_user_by_id(session, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.post("/", response_model=UserRead)
def create_user(data: UserCreate,session: SessionDep,user = Depends(require_roles([UserRole.admin, UserRole.analyst]))):
    try:
        return create_user_admin(session, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{user_id}", response_model=UserRead)
def update_user_route(user_id: int,data: UserUpdate,session: SessionDep,user = Depends(require_roles([UserRole.admin, UserRole.analyst]))):
    db_user = get_user_by_id(session, user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return update_user(session, db_user, data)


@router.delete("/{user_id}")
def delete_user_route(user_id: int,session: SessionDep,user = Depends(require_roles([UserRole.admin, UserRole.analyst]))):
    db_user = get_user_by_id(session, user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    delete_user(session, db_user)
    return {"message": "User deleted"}