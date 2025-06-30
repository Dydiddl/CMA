from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from decimal import Decimal
from pydantic import BaseModel
from ..db.database import get_db
from ..models.contract import Contract as ContractModel

router = APIRouter()

class ContractBase(BaseModel):
    project_name: str
    contract_amount: Decimal
    contract_date: date
    vendor_id: str
    status: str = "진행중"
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    documents: Optional[dict] = None
    checklist: Optional[dict] = None

class ContractCreate(ContractBase):
    pass

class Contract(ContractBase):
    id: str
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True

@router.post("/", response_model=Contract)
async def create_contract(contract: ContractCreate, db: Session = Depends(get_db)):
    """새 계약을 생성합니다."""
    try:
        db_contract = ContractModel(**contract.dict())
        db.add(db_contract)
        db.commit()
        db.refresh(db_contract)
        return db_contract
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"계약 생성 실패: {str(e)}")

@router.get("/", response_model=List[Contract])
async def get_contracts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """계약 목록을 조회합니다."""
    try:
        contracts = db.query(ContractModel).offset(skip).limit(limit).all()
        return contracts
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"계약 목록 조회 실패: {str(e)}")

@router.get("/{contract_id}", response_model=Contract)
async def get_contract(contract_id: str, db: Session = Depends(get_db)):
    """특정 계약의 상세 정보를 조회합니다."""
    try:
        contract = db.query(ContractModel).filter(ContractModel.id == contract_id).first()
        if not contract:
            raise HTTPException(status_code=404, detail="계약을 찾을 수 없습니다.")
        return contract
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"계약 조회 실패: {str(e)}")

@router.put("/{contract_id}", response_model=Contract)
async def update_contract(contract_id: str, contract: ContractCreate, db: Session = Depends(get_db)):
    """계약 정보를 수정합니다."""
    try:
        db_contract = db.query(ContractModel).filter(ContractModel.id == contract_id).first()
        if not db_contract:
            raise HTTPException(status_code=404, detail="계약을 찾을 수 없습니다.")
        
        for key, value in contract.dict().items():
            setattr(db_contract, key, value)
        
        db.commit()
        db.refresh(db_contract)
        return db_contract
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"계약 수정 실패: {str(e)}")

@router.delete("/{contract_id}")
async def delete_contract(contract_id: str, db: Session = Depends(get_db)):
    """계약을 삭제합니다."""
    try:
        db_contract = db.query(ContractModel).filter(ContractModel.id == contract_id).first()
        if not db_contract:
            raise HTTPException(status_code=404, detail="계약을 찾을 수 없습니다.")
        
        db.delete(db_contract)
        db.commit()
        return {"message": "계약이 성공적으로 삭제되었습니다."}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"계약 삭제 실패: {str(e)}") 