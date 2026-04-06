from sqlmodel import Session, select
from models.transaction import TransactionRecord, TransactionType
from collections import defaultdict


def get_summary(session: Session, user_id: int):
    records = session.exec(
        select(TransactionRecord).where(TransactionRecord.user_id == user_id)
    ).all()

    total_income = 0
    total_expense = 0

    for r in records:
        if r.type == TransactionType.income:
            total_income += r.amount
        else:
            total_expense += r.amount

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": total_income - total_expense
    }

def get_category_summary(session: Session, user_id: int):
    records = session.exec(
        select(TransactionRecord).where(TransactionRecord.user_id == user_id)
    ).all()

    category_data = defaultdict(float)

    for r in records:
        category_data[r.category] += r.amount

    return category_data

def get_recent_transactions(session: Session, user_id: int, limit: int = 5):
    records = session.exec(select(TransactionRecord).where(TransactionRecord.user_id == user_id).order_by(TransactionRecord.date.desc()).limit(limit)).all()
    return records