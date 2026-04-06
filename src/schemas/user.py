from pydantic import BaseModel, EmailStr
from models.user import UserRole
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.viewer

class UserRead(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: UserRole
    status: bool
    created_at: datetime

class UserUpdate(BaseModel):
    name: str | None = None
    role: UserRole | None = None
    status: bool | None = None