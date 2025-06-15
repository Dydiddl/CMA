from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.core.permissions import check_permissions
from app.models.user import User
from app.schemas.contract import (
    ContractCreate, ContractUpdate, Contract,
    ContractAmendment, ContractAmendmentCreate, ContractAmendmentUpdate,
    ContractPayment, ContractPaymentCreate, ContractPaymentUpdate,
    ContractFilter, ContractAmendmentFilter, ContractPaymentFilter
)
from app.crud import contract as contract_crud

router = APIRouter()

# 계약 기본 CRUD
@router.post("/", response_model=Contract)
def create_contract(
    *,
    db: Session = Depends(deps.get_db),
    contract_in: ContractCreate,
    current_user: User = Depends(deps.get_current_user)
) -> Contract:
    """
    새로운 계약을 생성합니다.
    """
    if not check_permissions(current_user, ["create:contract"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="계약 생성 권한이 없습니다"
        )
    
    contract = contract_crud.create(db=db, obj_in=contract_in, creator_id=current_user.id)
    return contract

@router.get("/", response_model=List[Contract])
def read_contracts(
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
    department_id: Optional[int] = None,
    current_user: User = Depends(deps.get_current_user)
) -> List[Contract]:
    """
    계약 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:contract"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="계약 조회 권한이 없습니다"
        )
    
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
    contracts = contract_crud.get_multi(
        db=db,
        skip=skip,
        limit=limit,
        filters=filters.dict(exclude_none=True)
    )
    return contracts

@router.get("/{contract_id}", response_model=Contract)
def read_contract(
    *,
    db: Session = Depends(deps.get_db),
    contract_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> Contract:
    """
    특정 계약을 조회합니다.
    """
    if not check_permissions(current_user, ["read:contract"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="계약 조회 권한이 없습니다"
        )
    
    contract = contract_crud.get(db=db, id=contract_id)
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="계약을 찾을 수 없습니다"
        )
    return contract

@router.put("/{contract_id}", response_model=Contract)
def update_contract(
    *,
    db: Session = Depends(deps.get_db),
    contract_id: int,
    contract_in: ContractUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> Contract:
    """
    계약 정보를 업데이트합니다.
    """
    if not check_permissions(current_user, ["update:contract"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="계약 수정 권한이 없습니다"
        )
    
    contract = contract_crud.get(db=db, id=contract_id)
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="계약을 찾을 수 없습니다"
        )
    
    contract = contract_crud.update(db=db, db_obj=contract, obj_in=contract_in)
    return contract

@router.delete("/{contract_id}")
def delete_contract(
    *,
    db: Session = Depends(deps.get_db),
    contract_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> dict:
    """
    계약을 삭제합니다.
    """
    if not check_permissions(current_user, ["delete:contract"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="계약 삭제 권한이 없습니다"
        )
    
    contract = contract_crud.get(db=db, id=contract_id)
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="계약을 찾을 수 없습니다"
        )
    
    contract_crud.remove(db=db, id=contract_id)
    return {"message": "계약이 삭제되었습니다"}

# 계약 변경 관리
@router.post("/{contract_id}/amendments", response_model=ContractAmendment)
def create_amendment(
    *,
    db: Session = Depends(deps.get_db),
    contract_id: int,
    amendment_in: ContractAmendmentCreate,
    current_user: User = Depends(deps.get_current_user)
) -> ContractAmendment:
    """
    계약 변경 사항을 생성합니다.
    """
    if not check_permissions(current_user, ["create:contract_amendment"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="계약 변경 권한이 없습니다"
        )
    
    contract = contract_crud.get(db=db, id=contract_id)
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="계약을 찾을 수 없습니다"
        )
    
    amendment = contract_crud.create_amendment(
        db=db,
        contract_id=contract_id,
        amendment_in=amendment_in,
        creator_id=current_user.id
    )
    return amendment

@router.get("/{contract_id}/amendments", response_model=List[ContractAmendment])
def read_amendments(
    *,
    db: Session = Depends(deps.get_db),
    contract_id: int,
    skip: int = 0,
    limit: int = 100,
    amendment_date_from: Optional[str] = None,
    amendment_date_to: Optional[str] = None,
    status: Optional[str] = None,
    approved_by: Optional[int] = None,
    current_user: User = Depends(deps.get_current_user)
) -> List[ContractAmendment]:
    """
    계약 변경사항 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:contract_amendment"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="계약 변경 조회 권한이 없습니다"
        )
    
    filters = ContractAmendmentFilter(
        contract_id=contract_id,
        amendment_date_from=amendment_date_from,
        amendment_date_to=amendment_date_to,
        status=status,
        approved_by=approved_by
    )
    amendments = contract_crud.get_amendments(
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
    amendment_in: ContractAmendmentUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> ContractAmendment:
    """
    계약 변경사항을 업데이트합니다.
    """
    if not check_permissions(current_user, ["update:contract_amendment"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="계약 변경 수정 권한이 없습니다"
        )
    
    amendment = contract_crud.get_amendment(db=db, amendment_id=amendment_id)
    if not amendment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="계약 변경사항을 찾을 수 없습니다"
        )
    
    amendment = contract_crud.update_amendment(
        db=db,
        amendment_id=amendment_id,
        amendment_in=amendment_in
    )
    return amendment

@router.delete("/amendments/{amendment_id}")
def delete_amendment(
    *,
    db: Session = Depends(deps.get_db),
    amendment_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> dict:
    """
    계약 변경사항을 삭제합니다.
    """
    if not check_permissions(current_user, ["delete:contract_amendment"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="계약 변경 삭제 권한이 없습니다"
        )
    
    amendment = contract_crud.get_amendment(db=db, amendment_id=amendment_id)
    if not amendment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="계약 변경사항을 찾을 수 없습니다"
        )
    
    contract_crud.delete_amendment(db=db, amendment_id=amendment_id)
    return {"message": "계약 변경사항이 삭제되었습니다"}

# 계약 지불 관리
@router.post("/{contract_id}/payments", response_model=ContractPayment)
def create_payment(
    *,
    db: Session = Depends(deps.get_db),
    contract_id: int,
    payment_in: ContractPaymentCreate,
    current_user: User = Depends(deps.get_current_user)
) -> ContractPayment:
    """
    계약 지불 내역을 생성합니다.
    """
    if not check_permissions(current_user, ["create:contract_payment"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="지불 내역 생성 권한이 없습니다"
        )
    
    contract = contract_crud.get(db=db, id=contract_id)
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="계약을 찾을 수 없습니다"
        )
    
    payment = contract_crud.create_payment(
        db=db,
        contract_id=contract_id,
        payment_in=payment_in,
        creator_id=current_user.id
    )
    return payment

@router.get("/{contract_id}/payments", response_model=List[ContractPayment])
def read_payments(
    *,
    db: Session = Depends(deps.get_db),
    contract_id: int,
    skip: int = 0,
    limit: int = 100,
    due_date_from: Optional[str] = None,
    due_date_to: Optional[str] = None,
    status: Optional[str] = None,
    payment_date_from: Optional[str] = None,
    payment_date_to: Optional[str] = None,
    current_user: User = Depends(deps.get_current_user)
) -> List[ContractPayment]:
    """
    계약 지불 내역 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:contract_payment"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="지불 내역 조회 권한이 없습니다"
        )
    
    filters = ContractPaymentFilter(
        contract_id=contract_id,
        due_date_from=due_date_from,
        due_date_to=due_date_to,
        status=status,
        payment_date_from=payment_date_from,
        payment_date_to=payment_date_to
    )
    payments = contract_crud.get_payments(
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
    payment_in: ContractPaymentUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> ContractPayment:
    """
    계약 지불 내역을 업데이트합니다.
    """
    if not check_permissions(current_user, ["update:contract_payment"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="지불 내역 수정 권한이 없습니다"
        )
    
    payment = contract_crud.get_payment(db=db, payment_id=payment_id)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="계약 지불 내역을 찾을 수 없습니다"
        )
    
    payment = contract_crud.update_payment(
        db=db,
        payment_id=payment_id,
        payment_in=payment_in
    )
    return payment

@router.delete("/payments/{payment_id}")
def delete_payment(
    *,
    db: Session = Depends(deps.get_db),
    payment_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> dict:
    """
    계약 지불 내역을 삭제합니다.
    """
    if not check_permissions(current_user, ["delete:contract_payment"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="지불 내역 삭제 권한이 없습니다"
        )
    
    payment = contract_crud.get_payment(db=db, payment_id=payment_id)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="계약 지불 내역을 찾을 수 없습니다"
        )
    
    contract_crud.delete_payment(db=db, payment_id=payment_id)
    return {"message": "계약 지불 내역이 삭제되었습니다"} 