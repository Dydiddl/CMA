from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import contract as crud
from app.schemas.contract import (
    Contract, ContractCreate, ContractUpdate,
    ContractAmendment, ContractAmendmentCreate, ContractAmendmentUpdate,
    ContractPayment, ContractPaymentCreate, ContractPaymentUpdate,
    ContractFilter, ContractAmendmentFilter, ContractPaymentFilter
)

router = APIRouter()

# Contract 엔드포인트
@router.post("/", response_model=Contract)
def create_contract(
    *,
    db: Session = Depends(deps.get_db),
    contract_in: ContractCreate
) -> Contract:
    """
    새로운 계약을 생성합니다.
    """
    contract = crud.create_contract(db=db, contract=contract_in)
    return contract

@router.get("/{contract_id}", response_model=Contract)
def get_contract(
    *,
    db: Session = Depends(deps.get_db),
    contract_id: int
) -> Contract:
    """
    ID로 계약을 조회합니다.
    """
    contract = crud.get_contract(db=db, contract_id=contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="계약을 찾을 수 없습니다")
    return contract

@router.get("/", response_model=List[Contract])
def get_contracts(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    contract_number: Optional[str] = None,
    contract_type: Optional[str] = None,
    status: Optional[str] = None,
    client_name: Optional[str] = None,
    start_date_from: Optional[str] = None,
    start_date_to: Optional[str] = None,
    end_date_from: Optional[str] = None,
    end_date_to: Optional[str] = None,
    manager_id: Optional[int] = None,
    department_id: Optional[int] = None
) -> List[Contract]:
    """
    계약 목록을 조회합니다.
    """
    filters = ContractFilter(
        contract_number=contract_number,
        contract_type=contract_type,
        status=status,
        client_name=client_name,
        start_date_from=start_date_from,
        start_date_to=start_date_to,
        end_date_from=end_date_from,
        end_date_to=end_date_to,
        manager_id=manager_id,
        department_id=department_id
    )
    contracts = crud.get_contracts(
        db=db,
        skip=skip,
        limit=limit,
        filters=filters.dict(exclude_none=True)
    )
    return contracts

@router.put("/{contract_id}", response_model=Contract)
def update_contract(
    *,
    db: Session = Depends(deps.get_db),
    contract_id: int,
    contract_in: ContractUpdate
) -> Contract:
    """
    계약을 업데이트합니다.
    """
    contract = crud.get_contract(db=db, contract_id=contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="계약을 찾을 수 없습니다")
    contract = crud.update_contract(
        db=db,
        contract_id=contract_id,
        contract=contract_in
    )
    return contract

@router.delete("/{contract_id}")
def delete_contract(
    *,
    db: Session = Depends(deps.get_db),
    contract_id: int
) -> dict:
    """
    계약을 삭제합니다.
    """
    contract = crud.get_contract(db=db, contract_id=contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="계약을 찾을 수 없습니다")
    crud.delete_contract(db=db, contract_id=contract_id)
    return {"message": "계약이 삭제되었습니다"}

# ContractAmendment 엔드포인트
@router.post("/{contract_id}/amendments", response_model=ContractAmendment)
def create_amendment(
    *,
    db: Session = Depends(deps.get_db),
    contract_id: int,
    amendment_in: ContractAmendmentCreate
) -> ContractAmendment:
    """
    새로운 계약 변경사항을 생성합니다.
    """
    contract = crud.get_contract(db=db, contract_id=contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="계약을 찾을 수 없습니다")
    amendment = crud.create_amendment(db=db, amendment=amendment_in)
    return amendment

@router.get("/{contract_id}/amendments", response_model=List[ContractAmendment])
def get_amendments(
    *,
    db: Session = Depends(deps.get_db),
    contract_id: int,
    skip: int = 0,
    limit: int = 100,
    amendment_date_from: Optional[str] = None,
    amendment_date_to: Optional[str] = None,
    status: Optional[str] = None,
    approved_by: Optional[int] = None
) -> List[ContractAmendment]:
    """
    계약 변경사항 목록을 조회합니다.
    """
    filters = ContractAmendmentFilter(
        contract_id=contract_id,
        amendment_date_from=amendment_date_from,
        amendment_date_to=amendment_date_to,
        status=status,
        approved_by=approved_by
    )
    amendments = crud.get_amendments(
        db=db,
        skip=skip,
        limit=limit,
        filters=filters.dict(exclude_none=True)
    )
    return amendments

@router.put("/amendments/{amendment_id}", response_model=ContractAmendment)
def update_amendment(
    *,
    db: Session = Depends(deps.get_db),
    amendment_id: int,
    amendment_in: ContractAmendmentUpdate
) -> ContractAmendment:
    """
    계약 변경사항을 업데이트합니다.
    """
    amendment = crud.get_amendment(db=db, amendment_id=amendment_id)
    if not amendment:
        raise HTTPException(status_code=404, detail="계약 변경사항을 찾을 수 없습니다")
    amendment = crud.update_amendment(
        db=db,
        amendment_id=amendment_id,
        amendment=amendment_in
    )
    return amendment

@router.delete("/amendments/{amendment_id}")
def delete_amendment(
    *,
    db: Session = Depends(deps.get_db),
    amendment_id: int
) -> dict:
    """
    계약 변경사항을 삭제합니다.
    """
    amendment = crud.get_amendment(db=db, amendment_id=amendment_id)
    if not amendment:
        raise HTTPException(status_code=404, detail="계약 변경사항을 찾을 수 없습니다")
    crud.delete_amendment(db=db, amendment_id=amendment_id)
    return {"message": "계약 변경사항이 삭제되었습니다"}

# ContractPayment 엔드포인트
@router.post("/{contract_id}/payments", response_model=ContractPayment)
def create_payment(
    *,
    db: Session = Depends(deps.get_db),
    contract_id: int,
    payment_in: ContractPaymentCreate
) -> ContractPayment:
    """
    새로운 계약 지불 내역을 생성합니다.
    """
    contract = crud.get_contract(db=db, contract_id=contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="계약을 찾을 수 없습니다")
    payment = crud.create_payment(db=db, payment=payment_in)
    return payment

@router.get("/{contract_id}/payments", response_model=List[ContractPayment])
def get_payments(
    *,
    db: Session = Depends(deps.get_db),
    contract_id: int,
    skip: int = 0,
    limit: int = 100,
    due_date_from: Optional[str] = None,
    due_date_to: Optional[str] = None,
    status: Optional[str] = None,
    payment_date_from: Optional[str] = None,
    payment_date_to: Optional[str] = None
) -> List[ContractPayment]:
    """
    계약 지불 내역 목록을 조회합니다.
    """
    filters = ContractPaymentFilter(
        contract_id=contract_id,
        due_date_from=due_date_from,
        due_date_to=due_date_to,
        status=status,
        payment_date_from=payment_date_from,
        payment_date_to=payment_date_to
    )
    payments = crud.get_payments(
        db=db,
        skip=skip,
        limit=limit,
        filters=filters.dict(exclude_none=True)
    )
    return payments

@router.put("/payments/{payment_id}", response_model=ContractPayment)
def update_payment(
    *,
    db: Session = Depends(deps.get_db),
    payment_id: int,
    payment_in: ContractPaymentUpdate
) -> ContractPayment:
    """
    계약 지불 내역을 업데이트합니다.
    """
    payment = crud.get_payment(db=db, payment_id=payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="계약 지불 내역을 찾을 수 없습니다")
    payment = crud.update_payment(
        db=db,
        payment_id=payment_id,
        payment=payment_in
    )
    return payment

@router.delete("/payments/{payment_id}")
def delete_payment(
    *,
    db: Session = Depends(deps.get_db),
    payment_id: int
) -> dict:
    """
    계약 지불 내역을 삭제합니다.
    """
    payment = crud.get_payment(db=db, payment_id=payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="계약 지불 내역을 찾을 수 없습니다")
    crud.delete_payment(db=db, payment_id=payment_id)
    return {"message": "계약 지불 내역이 삭제되었습니다"} 