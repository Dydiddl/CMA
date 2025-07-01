from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.api.deps import get_db
from ....schemas.financial import (
    FinancialRecord,
    FinancialRecordCreate,
    FinancialRecordUpdate,
    FinancialDocument,
    FinancialDocumentCreate
)
from ....services import financial as financial_service

router = APIRouter()

@router.post("/", response_model=FinancialRecord, description="새로운 재무 기록을 생성합니다.")
def create_financial_record(
    record: FinancialRecordCreate,
    db: Session = Depends(get_db)
):
    """새로운 재무 기록을 생성합니다."""
    return financial_service.create_financial_record(db=db, record=record)

@router.get("/", response_model=List[FinancialRecord], description="재무 기록 목록을 조회합니다.")
def read_financial_records(
    skip: int = 0,
    limit: int = 100,
    type: Optional[str] = None,
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    contract_id: Optional[int] = None,
    vendor_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """재무 기록 목록을 조회합니다."""
    return financial_service.get_financial_records(
        db=db,
        skip=skip,
        limit=limit,
        type=type,
        category=category,
        start_date=start_date,
        end_date=end_date,
        contract_id=contract_id,
        vendor_id=vendor_id
    )

@router.get("/{record_id}", response_model=FinancialRecord, description="특정 재무 기록의 상세 정보를 조회합니다.")
def read_financial_record(
    record_id: int,
    db: Session = Depends(get_db)
):
    """특정 재무 기록의 상세 정보를 조회합니다."""
    record = financial_service.get_financial_record(db=db, record_id=record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="재무 기록을 찾을 수 없습니다")
    return record

@router.put("/{record_id}", response_model=FinancialRecord, description="재무 기록을 업데이트합니다.")
def update_financial_record(
    record_id: int,
    record: FinancialRecordUpdate,
    db: Session = Depends(get_db)
):
    """재무 기록을 업데이트합니다."""
    updated_record = financial_service.update_financial_record(
        db=db,
        record_id=record_id,
        record=record
    )
    if updated_record is None:
        raise HTTPException(status_code=404, detail="재무 기록을 찾을 수 없습니다")
    return updated_record

@router.delete("/{record_id}", description="재무 기록을 삭제합니다.")
def delete_financial_record(
    record_id: int,
    db: Session = Depends(get_db)
):
    """재무 기록을 삭제합니다."""
    success = financial_service.delete_financial_record(db=db, record_id=record_id)
    if not success:
        raise HTTPException(status_code=404, detail="재무 기록을 찾을 수 없습니다")
    return {"message": "재무 기록이 삭제되었습니다"}

@router.post("/{record_id}/documents", response_model=FinancialDocument, description="재무 기록에 문서를 추가합니다.")
def create_financial_document(
    record_id: int,
    document: FinancialDocumentCreate,
    db: Session = Depends(get_db)
):
    """재무 기록에 문서를 추가합니다."""
    return financial_service.create_financial_document(
        db=db,
        record_id=record_id,
        document=document
    )

@router.get("/{record_id}/documents", response_model=List[FinancialDocument], description="재무 기록의 모든 문서를 조회합니다.")
def read_financial_documents(
    record_id: int,
    db: Session = Depends(get_db)
):
    """재무 기록의 모든 문서를 조회합니다."""
    return financial_service.get_financial_documents(
        db=db,
        record_id=record_id
    ) 