from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.contract import Contract, ContractDocument
from app.schemas.contract import ContractCreate, ContractUpdate, ContractDocumentCreate

class ContractService:
    """계약 서비스 클래스"""
    def __init__(self, db: Session):
        self.db = db

    def create_contract(self, contract: ContractCreate) -> Contract:
        """새로운 계약을 생성합니다."""
        db_contract = Contract(**contract.dict())
        self.db.add(db_contract)
        self.db.commit()
        self.db.refresh(db_contract)
        return db_contract

    def get_contracts(self, skip: int = 0, limit: int = 100, status: Optional[str] = None) -> List[Contract]:
        """계약 목록을 조회합니다."""
        query = self.db.query(Contract)
        if status:
            query = query.filter(Contract.status == status)
        return query.offset(skip).limit(limit).all()

    def get_contract(self, contract_id: int) -> Optional[Contract]:
        """특정 계약을 조회합니다."""
        return self.db.query(Contract).filter(Contract.id == contract_id).first()

    def update_contract(self, contract_id: int, contract: ContractUpdate) -> Optional[Contract]:
        """계약 정보를 업데이트합니다."""
        db_contract = self.get_contract(contract_id)
        if db_contract:
            for key, value in contract.dict(exclude_unset=True).items():
                setattr(db_contract, key, value)
            self.db.commit()
            self.db.refresh(db_contract)
        return db_contract

    def delete_contract(self, contract_id: int) -> bool:
        """계약을 삭제합니다."""
        db_contract = self.get_contract(contract_id)
        if db_contract:
            self.db.delete(db_contract)
            self.db.commit()
            return True
        return False

    def create_contract_document(self, contract_id: int, document: ContractDocumentCreate) -> ContractDocument:
        """계약 문서를 생성합니다."""
        db_document = ContractDocument(
            **document.dict(),
            contract_id=contract_id
        )
        self.db.add(db_document)
        self.db.commit()
        self.db.refresh(db_document)
        return db_document

    def get_contract_documents(self, contract_id: int) -> List[ContractDocument]:
        """계약의 모든 문서를 조회합니다."""
        return self.db.query(ContractDocument).filter(
            ContractDocument.contract_id == contract_id
        ).all()

# 기존 함수도 유지 (호환성)
def create_contract(db: Session, contract: ContractCreate) -> Contract:
    return ContractService(db).create_contract(contract)
def get_contracts(db: Session, skip: int = 0, limit: int = 100, status: Optional[str] = None) -> List[Contract]:
    return ContractService(db).get_contracts(skip, limit, status)
def get_contract(db: Session, contract_id: int) -> Optional[Contract]:
    return ContractService(db).get_contract(contract_id)
def update_contract(db: Session, contract_id: int, contract: ContractUpdate) -> Optional[Contract]:
    return ContractService(db).update_contract(contract_id, contract)
def delete_contract(db: Session, contract_id: int) -> bool:
    return ContractService(db).delete_contract(contract_id)
def create_contract_document(db: Session, contract_id: int, document: ContractDocumentCreate) -> ContractDocument:
    return ContractService(db).create_contract_document(contract_id, document)
def get_contract_documents(db: Session, contract_id: int) -> List[ContractDocument]:
    return ContractService(db).get_contract_documents(contract_id) 