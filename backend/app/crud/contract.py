from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime

from app.models.contract import Contract, ContractAmendment, ContractPayment
from app.schemas.contract import (
    ContractCreate, ContractUpdate,
    ContractAmendmentCreate, ContractAmendmentUpdate,
    ContractPaymentCreate, ContractPaymentUpdate
)

# Contract CRUD
def create_contract(db: Session, contract: ContractCreate) -> Contract:
    db_contract = Contract(**contract.dict())
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract

def get_contract(db: Session, contract_id: int) -> Optional[Contract]:
    return db.query(Contract).filter(Contract.id == contract_id).first()

def get_contracts(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    filters: Optional[Dict[str, Any]] = None
) -> List[Contract]:
    query = db.query(Contract)
    
    if filters:
        if filters.get("contract_number"):
            query = query.filter(Contract.contract_number.ilike(f"%{filters['contract_number']}%"))
        if filters.get("contract_type"):
            query = query.filter(Contract.contract_type == filters["contract_type"])
        if filters.get("status"):
            query = query.filter(Contract.status == filters["status"])
        if filters.get("client_name"):
            query = query.filter(Contract.client_name.ilike(f"%{filters['client_name']}%"))
        if filters.get("start_date_from"):
            query = query.filter(Contract.start_date >= filters["start_date_from"])
        if filters.get("start_date_to"):
            query = query.filter(Contract.start_date <= filters["start_date_to"])
        if filters.get("end_date_from"):
            query = query.filter(Contract.end_date >= filters["end_date_from"])
        if filters.get("end_date_to"):
            query = query.filter(Contract.end_date <= filters["end_date_to"])
        if filters.get("manager_id"):
            query = query.filter(Contract.manager_id == filters["manager_id"])
        if filters.get("department_id"):
            query = query.filter(Contract.department_id == filters["department_id"])
    
    return query.offset(skip).limit(limit).all()

def update_contract(
    db: Session,
    contract_id: int,
    contract: ContractUpdate
) -> Optional[Contract]:
    db_contract = get_contract(db, contract_id)
    if db_contract:
        update_data = contract.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_contract, key, value)
        db.commit()
        db.refresh(db_contract)
    return db_contract

def delete_contract(db: Session, contract_id: int) -> bool:
    db_contract = get_contract(db, contract_id)
    if db_contract:
        db.delete(db_contract)
        db.commit()
        return True
    return False

# ContractAmendment CRUD
def create_amendment(
    db: Session,
    amendment: ContractAmendmentCreate
) -> ContractAmendment:
    db_amendment = ContractAmendment(**amendment.dict())
    db.add(db_amendment)
    db.commit()
    db.refresh(db_amendment)
    return db_amendment

def get_amendment(
    db: Session,
    amendment_id: int
) -> Optional[ContractAmendment]:
    return db.query(ContractAmendment).filter(ContractAmendment.id == amendment_id).first()

def get_amendments(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    filters: Optional[Dict[str, Any]] = None
) -> List[ContractAmendment]:
    query = db.query(ContractAmendment)
    
    if filters:
        if filters.get("contract_id"):
            query = query.filter(ContractAmendment.contract_id == filters["contract_id"])
        if filters.get("amendment_date_from"):
            query = query.filter(ContractAmendment.amendment_date >= filters["amendment_date_from"])
        if filters.get("amendment_date_to"):
            query = query.filter(ContractAmendment.amendment_date <= filters["amendment_date_to"])
        if filters.get("status"):
            query = query.filter(ContractAmendment.status == filters["status"])
        if filters.get("approved_by"):
            query = query.filter(ContractAmendment.approved_by == filters["approved_by"])
    
    return query.offset(skip).limit(limit).all()

def update_amendment(
    db: Session,
    amendment_id: int,
    amendment: ContractAmendmentUpdate
) -> Optional[ContractAmendment]:
    db_amendment = get_amendment(db, amendment_id)
    if db_amendment:
        update_data = amendment.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_amendment, key, value)
        db.commit()
        db.refresh(db_amendment)
    return db_amendment

def delete_amendment(db: Session, amendment_id: int) -> bool:
    db_amendment = get_amendment(db, amendment_id)
    if db_amendment:
        db.delete(db_amendment)
        db.commit()
        return True
    return False

# ContractPayment CRUD
def create_payment(
    db: Session,
    payment: ContractPaymentCreate
) -> ContractPayment:
    db_payment = ContractPayment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payment(
    db: Session,
    payment_id: int
) -> Optional[ContractPayment]:
    return db.query(ContractPayment).filter(ContractPayment.id == payment_id).first()

def get_payments(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    filters: Optional[Dict[str, Any]] = None
) -> List[ContractPayment]:
    query = db.query(ContractPayment)
    
    if filters:
        if filters.get("contract_id"):
            query = query.filter(ContractPayment.contract_id == filters["contract_id"])
        if filters.get("due_date_from"):
            query = query.filter(ContractPayment.due_date >= filters["due_date_from"])
        if filters.get("due_date_to"):
            query = query.filter(ContractPayment.due_date <= filters["due_date_to"])
        if filters.get("status"):
            query = query.filter(ContractPayment.status == filters["status"])
        if filters.get("payment_date_from"):
            query = query.filter(ContractPayment.payment_date >= filters["payment_date_from"])
        if filters.get("payment_date_to"):
            query = query.filter(ContractPayment.payment_date <= filters["payment_date_to"])
    
    return query.offset(skip).limit(limit).all()

def update_payment(
    db: Session,
    payment_id: int,
    payment: ContractPaymentUpdate
) -> Optional[ContractPayment]:
    db_payment = get_payment(db, payment_id)
    if db_payment:
        update_data = payment.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_payment, key, value)
        db.commit()
        db.refresh(db_payment)
    return db_payment

def delete_payment(db: Session, payment_id: int) -> bool:
    db_payment = get_payment(db, payment_id)
    if db_payment:
        db.delete(db_payment)
        db.commit()
        return True
    return False 