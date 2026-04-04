from typing import Annotated
from sqlmodel import SQLModel,Field
from pydantic import EmailStr
from enum import Enum
class UserRole(str,Enum):
    viewer="viewer"
    analyst="analyst"
    admin="admin"

class User(SQLModel,table=True):
    __tablename__ = "users" 
    
    id: int | None =Field(default=None,primary_key=True)
    name: str
    email: EmailStr = Field(unique=True)
    role: UserRole=Field(default=UserRole.viewer)
    password: str
