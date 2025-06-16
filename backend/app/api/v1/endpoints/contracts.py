from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ....db.base import get_db
from ....schemas.contract import (
    Contract,
    ContractCreate,
    ContractUpdate,
    ContractDocument,
    ContractDocumentCreate
)
from ....services import contract as contract_service

router = APIRouter()

@router.post("/", response_model=Contract, description="새로운 계약을 생성합니다.")
def create_contract(
    contract: ContractCreate,
    db: Session = Depends(get_db)
):
    """새로운 계약을 생성합니다."""
    return contract_service.create_contract(db=db, contract=contract)

@router.get("/", response_model=List[Contract], description="계약 목록을 조회합니다.")
def read_contracts(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    vendor_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """계약 목록을 조회합니다."""
    return contract_service.get_contracts(
        db=db,
        skip=skip,
        limit=limit,
        status=status,
        vendor_id=vendor_id
    )

@router.get("/{contract_id}", response_model=Contract, description="특정 계약의 상세 정보를 조회합니다.")
def read_contract(
    contract_id: int,
    db: Session = Depends(get_db)
):
    """특정 계약의 상세 정보를 조회합니다."""
    contract = contract_service.get_contract(db=db, contract_id=contract_id)
    if contract is None:
        raise HTTPException(status_code=404, detail="계약을 찾을 수 없습니다")
    return contract

@router.put("/{contract_id}", response_model=Contract, description="계약 정보를 업데이트합니다.")
def update_contract(
    contract_id: int,
    contract: ContractUpdate,
    db: Session = Depends(get_db)
):
    """계약 정보를 업데이트합니다."""
    updated_contract = contract_service.update_contract(
        db=db,
        contract_id=contract_id,
        contract=contract
    )
    if updated_contract is None:
        raise HTTPException(status_code=404, detail="계약을 찾을 수 없습니다")
    return updated_contract

@router.delete("/{contract_id}", description="계약을 삭제합니다.")
def delete_contract(
    contract_id: int,
    db: Session = Depends(get_db)
):
    """계약을 삭제합니다."""
    success = contract_service.delete_contract(db=db, contract_id=contract_id)
    if not success:
        raise HTTPException(status_code=404, detail="계약을 찾을 수 없습니다")
    return {"message": "계약이 삭제되었습니다"}

@router.post("/{contract_id}/documents", response_model=ContractDocument, description="계약에 문서를 추가합니다.")
def create_contract_document(
    contract_id: int,
    document: ContractDocumentCreate,
    db: Session = Depends(get_db)
):
    """계약에 문서를 추가합니다."""
    return contract_service.create_contract_document(
        db=db,
        contract_id=contract_id,
        document=document
    )

@router.get("/{contract_id}/documents", response_model=List[ContractDocument], description="계약의 모든 문서를 조회합니다.")
def read_contract_documents(
    contract_id: int,
    db: Session = Depends(get_db)
):
    """계약의 모든 문서를 조회합니다."""
    return contract_service.get_contract_documents(
        db=db,
        contract_id=contract_id
    ) 