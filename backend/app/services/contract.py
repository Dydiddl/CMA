from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.contract import Contract, ContractDocument
from ..schemas.contract import ContractCreate, ContractUpdate, ContractDocumentCreate

def create_contract(db: Session, contract: ContractCreate) -> Contract:
    """새로운 계약을 생성합니다."""
    db_contract = Contract(**contract.dict())
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract

def get_contracts(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None
) -> List[Contract]:
    """계약 목록을 조회합니다."""
    query = db.query(Contract)
    if status:
        query = query.filter(Contract.status == status)
    return query.offset(skip).limit(limit).all()

def get_contract(db: Session, contract_id: int) -> Optional[Contract]:
    """특정 계약을 조회합니다."""
    return db.query(Contract).filter(Contract.id == contract_id).first()

def update_contract(
    db: Session,
    contract_id: int,
    contract: ContractUpdate
) -> Optional[Contract]:
    """계약 정보를 업데이트합니다."""
    db_contract = get_contract(db, contract_id)
    if db_contract:
        for key, value in contract.dict(exclude_unset=True).items():
            setattr(db_contract, key, value)
        db.commit()
        db.refresh(db_contract)
    return db_contract

def delete_contract(db: Session, contract_id: int) -> bool:
    """계약을 삭제합니다."""
    db_contract = get_contract(db, contract_id)
    if db_contract:
        db.delete(db_contract)
        db.commit()
        return True
    return False

def create_contract_document(
    db: Session,
    contract_id: int,
    document: ContractDocumentCreate
) -> ContractDocument:
    """계약 문서를 생성합니다."""
    db_document = ContractDocument(
        **document.dict(),
        contract_id=contract_id
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_contract_documents(
    db: Session,
    contract_id: int
) -> List[ContractDocument]:
    """계약의 모든 문서를 조회합니다."""
    return db.query(ContractDocument).filter(
        ContractDocument.contract_id == contract_id
    ).all() 