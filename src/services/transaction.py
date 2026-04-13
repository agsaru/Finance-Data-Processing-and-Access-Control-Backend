from sqlmodel import Session, select
from models.transaction import TransactionRecord
from schemas.transaction import TransactionCreate, TransactionUpdate
from models.user import UserRole
def create_record(session: Session, data: TransactionCreate, user_id: int):
    record = TransactionRecord(
        amount=data.amount,
        type=data.type,
        category=data.category,
        description=data.description,
        date=data.date,
        user_id=user_id
    )

    session.add(record)
    session.commit()
    session.refresh(record)

    return record

def get_records(session: Session, user_id: int,user_role: UserRole, type=None, category=None):
    query = select(TransactionRecord).where(TransactionRecord.user_id == user_id)
    if user_role != UserRole.admin:
        query = query.where(TransactionRecord.user_id == user_id)
    if type:
        query = query.where(TransactionRecord.type == type)

    if category:
        query = query.where(TransactionRecord.category == category)

    return session.exec(query).all()

def get_record_by_id(session: Session, record_id: int):
    return session.get(TransactionRecord, record_id)

def update_record(session: Session, record: TransactionRecord, data: TransactionUpdate):
    if data.amount is not None:
        record.amount = data.amount

    if data.type is not None:
        record.type = data.type

    if data.category is not None:
        record.category = data.category
        
    if data.description is not None:
        record.description = data.description

    if data.date is not None:
        record.date = data.date

    session.add(record)
    session.commit()
    session.refresh(record)

    return record

def delete_record(session: Session, record: TransactionRecord):
    session.delete(record)
    session.commit()