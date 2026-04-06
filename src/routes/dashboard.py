from fastapi import APIRouter, Depends
from sqlmodel import Session
from config.database import SessionDep
from config.security import get_current_user
from services.dashboard import get_summary, get_category_summary, get_recent_transactions
from schemas.transaction import TransactionRead

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary")
def summary(session: SessionDep, user = Depends(get_current_user)):
    return get_summary(session, user.id)

@router.get("/category-summary")
def category_summary(session: SessionDep, user = Depends(get_current_user)):
    return get_category_summary(session, user.id)

@router.get("/recent", response_model=list[TransactionRead])
def recent_transactions(session: SessionDep, user = Depends(get_current_user)):
    return get_recent_transactions(session, user.id)