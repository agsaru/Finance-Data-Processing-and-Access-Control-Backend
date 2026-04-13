from sqlmodel import Session, select, func
from models.transaction import TransactionRecord, TransactionType

def get_summary(session: Session, user_id: int,role: str):
    records = select(func.coalesce(func.sum(TransactionRecord.amount), 0)).where(
        TransactionRecord.user_id == user_id,
        TransactionRecord.type == TransactionType.income
    )
    expense = select(func.coalesce(func.sum(TransactionRecord.amount), 0)).where(
        TransactionRecord.user_id == user_id,
        TransactionRecord.type == TransactionType.expense
    )
    if role != "admin":
        income_query = income_query.where(TransactionRecord.user_id == user_id)
        expense_query = expense_query.where(TransactionRecord.user_id == user_id)

    total_income = session.exec(income_query).one()
    total_expense = session.exec(expense_query).one()
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": total_income - total_expense
    }

def get_category_summary(session: Session, user_id: int):
    records = (
        select(TransactionRecord.category, func.sum(TransactionRecord.amount))
        .where(TransactionRecord.user_id == user_id)
        .group_by(TransactionRecord.category)
    )
    
    results = session.exec(records).all()
    return {category: amount for category, amount in results}

def get_recent_transactions(session: Session, user_id: int, limit: int = 5):
    records = (
        select(TransactionRecord)
        .where(TransactionRecord.user_id == user_id)
        .order_by(TransactionRecord.date.desc())
        .limit(limit)
    )
    return session.exec(records).all()