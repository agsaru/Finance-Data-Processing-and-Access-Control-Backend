from sqlmodel import SQLModel, create_engine, Session
from fastapi import Depends
from typing import Annotated, TypeAlias
from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL")
engine=create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep: TypeAlias=Annotated[Session,Depends(get_session)]