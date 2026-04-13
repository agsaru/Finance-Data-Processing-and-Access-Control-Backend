from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from config.database import SessionDep
from config.security import require_roles
from models.user import UserRole
from schemas.transaction import TransactionCreate, TransactionRead, TransactionUpdate
from services.transaction import (
    create_record,
    get_records,
    get_record_by_id,
    update_record,
    delete_record
)

router = APIRouter(prefix="/financial", tags=["Financial"])

@router.post("/", response_model=TransactionRead)
def create_financial_record(data: TransactionCreate, session: SessionDep, user = Depends(require_roles([UserRole.admin]))):
    return create_record(session, data, user.id)

@router.get("/", response_model=list[TransactionRead])
def read_records(session: SessionDep, user = Depends(require_roles([UserRole.admin, UserRole.analyst])), type: str | None = Query(default=None), category: str | None = Query(default=None)):
    return get_records(session, user.id,user.role, type, category)

@router.get("/{record_id}", response_model=TransactionRead)
def read_record(record_id: int, session: SessionDep, user = Depends(require_roles([UserRole.admin, UserRole.analyst]))):
    record = get_record_by_id(session, record_id)

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    if record.user_id != user.id and user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    return record


@router.patch("/{record_id}", response_model=TransactionRead)
def update_financial_record(record_id: int, data: TransactionUpdate, session: SessionDep, user = Depends(require_roles([UserRole.admin]))):
    record = get_record_by_id(session, record_id)

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    if record.user_id != user.id and user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    return update_record(session, record, data)


@router.delete("/{record_id}")
def delete_financial_record(record_id: int, session: SessionDep, user = Depends(require_roles([UserRole.admin]))):
    record = get_record_by_id(session, record_id)

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    if record.user_id != user.id and user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    delete_record(session, record)
    return {"message": "Record deleted"}