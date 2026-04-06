from pydantic import BaseModel
from datetime import datetime
from models.transaction import TransactionType

class TransactionCreate(BaseModel):
    amount: float
    type: TransactionType
    category: str
    date: datetime | None = None

class TransactionRead(BaseModel):
    id: int
    amount: float
    type: TransactionType
    category: str
    description: str | None = None
    date: datetime
    user_id: int
    
class TransactionUpdate(BaseModel):
    amount: float | None = None
    type: TransactionType | None = None
    category: str | None = None
    date: datetime | None = None