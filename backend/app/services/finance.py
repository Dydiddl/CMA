from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from ..models.financial import FinancialRecord, FinancialDocument
from ..schemas.financial import (
    FinancialRecordCreate,
    FinancialRecordUpdate,
    FinancialDocumentCreate
)

def create_transaction(
    db: Session,
    transaction: FinancialRecordCreate
) -> FinancialRecord:
    """새로운 재무 거래를 등록합니다."""
    db_transaction = FinancialRecord(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    transaction_type: Optional[str] = None
) -> List[FinancialRecord]:
    """재무 거래 목록을 조회합니다."""
    query = db.query(FinancialRecord)
    if start_date:
        query = query.filter(FinancialRecord.transaction_date >= start_date)
    if end_date:
        query = query.filter(FinancialRecord.transaction_date <= end_date)
    if transaction_type:
        query = query.filter(FinancialRecord.type == transaction_type)
    return query.offset(skip).limit(limit).all()

def get_transaction(
    db: Session,
    transaction_id: int
) -> Optional[FinancialRecord]:
    """특정 재무 거래의 정보를 조회합니다."""
    return db.query(FinancialRecord).filter(
        FinancialRecord.id == transaction_id
    ).first()

def update_transaction(
    db: Session,
    transaction_id: int,
    transaction: FinancialRecordUpdate
) -> Optional[FinancialRecord]:
    """재무 거래 정보를 업데이트합니다."""
    db_transaction = get_transaction(db, transaction_id)
    if db_transaction:
        for key, value in transaction.dict(exclude_unset=True).items():
            setattr(db_transaction, key, value)
        db.commit()
        db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, transaction_id: int) -> bool:
    """재무 거래를 삭제합니다."""
    db_transaction = get_transaction(db, transaction_id)
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
        return True
    return False

def create_financial_document(
    db: Session,
    document: FinancialDocumentCreate
) -> FinancialDocument:
    """재무 문서를 생성합니다."""
    db_document = FinancialDocument(**document.dict())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_financial_documents(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    document_type: Optional[str] = None
) -> List[FinancialDocument]:
    """재무 문서 목록을 조회합니다."""
    query = db.query(FinancialDocument)
    if document_type:
        query = query.filter(FinancialDocument.type == document_type)
    return query.offset(skip).limit(limit).all()

def get_financial_document(
    db: Session,
    document_id: int
) -> Optional[FinancialDocument]:
    """특정 재무 문서의 정보를 조회합니다."""
    return db.query(FinancialDocument).filter(
        FinancialDocument.id == document_id
    ).first() 