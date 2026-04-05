from typing import Annotated
from sqlmodel import SQLModel,Field
from pydantic import EmailStr
from enum import Enum
from datetime import datetime,timezone
class UserRole(str,Enum):
    viewer="viewer"
    analyst="analyst"
    admin="admin"

class User(SQLModel,table=True):
    __tablename__ = "users" 

    id: int | None = Field(default=None,primary_key=True)
    name: str
    email: EmailStr = Field(unique=True)
    role: UserRole= Field(default=UserRole.viewer)
    password: str
    created_at: datetime= Field(default_factory=lambda: datetime.now(timezone.utc))
    status: bool = True
