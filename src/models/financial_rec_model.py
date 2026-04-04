from sqlmodel import SQLModel,Field
from enum import Enum
from datetime import datetime, timezone
class TransationType(str,Enum):
    income="income"
    expense="expense"

class FinancialRecord(SQLModel,table=True):
    __tablename__ = "financialrecords" 

    id: int | None =Field(default=None, primary_key=True)
    amount:float
    type: TransationType
    category:str
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user_id: int =Field(foreign_key="user.id")