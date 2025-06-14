from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime

from app.models.document import Document, DocumentVersion, DocumentApproval
from app.schemas.document import (
    DocumentCreate, DocumentUpdate,
    DocumentVersionCreate, DocumentVersionUpdate,
    DocumentApprovalCreate, DocumentApprovalUpdate
)

# Document CRUD
def create_document(db: Session, document: DocumentCreate, created_by: int) -> Document:
    db_document = Document(
        **document.dict(),
        created_by=created_by,
        updated_by=created_by
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_document(db: Session, document_id: int) -> Optional[Document]:
    return db.query(Document).filter(Document.id == document_id).first()

def get_documents(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    filters: Optional[Dict[str, Any]] = None
) -> List[Document]:
    query = db.query(Document)
    
    if filters:
        if filters.get("document_number"):
            query = query.filter(Document.document_number.ilike(f"%{filters['document_number']}%"))
        if filters.get("title"):
            query = query.filter(Document.title.ilike(f"%{filters['title']}%"))
        if filters.get("document_type"):
            query = query.filter(Document.document_type == filters["document_type"])
        if filters.get("status"):
            query = query.filter(Document.status == filters["status"])
        if filters.get("construction_id"):
            query = query.filter(Document.construction_id == filters["construction_id"])
        if filters.get("contract_id"):
            query = query.filter(Document.contract_id == filters["contract_id"])
        if filters.get("department_id"):
            query = query.filter(Document.department_id == filters["department_id"])
        if filters.get("created_by"):
            query = query.filter(Document.created_by == filters["created_by"])
        if filters.get("created_at_from"):
            query = query.filter(Document.created_at >= filters["created_at_from"])
        if filters.get("created_at_to"):
            query = query.filter(Document.created_at <= filters["created_at_to"])
    
    return query.offset(skip).limit(limit).all()

def update_document(
    db: Session,
    document_id: int,
    document: DocumentUpdate,
    updated_by: int
) -> Optional[Document]:
    db_document = get_document(db, document_id)
    if db_document:
        update_data = document.dict(exclude_unset=True)
        update_data["updated_by"] = updated_by
        for key, value in update_data.items():
            setattr(db_document, key, value)
        db.commit()
        db.refresh(db_document)
    return db_document

def delete_document(db: Session, document_id: int) -> bool:
    db_document = get_document(db, document_id)
    if db_document:
        db.delete(db_document)
        db.commit()
        return True
    return False

# DocumentVersion CRUD
def create_version(
    db: Session,
    version: DocumentVersionCreate,
    created_by: int
) -> DocumentVersion:
    db_version = DocumentVersion(
        **version.dict(),
        created_by=created_by
    )
    db.add(db_version)
    db.commit()
    db.refresh(db_version)
    return db_version

def get_version(
    db: Session,
    version_id: int
) -> Optional[DocumentVersion]:
    return db.query(DocumentVersion).filter(DocumentVersion.id == version_id).first()

def get_versions(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    filters: Optional[Dict[str, Any]] = None
) -> List[DocumentVersion]:
    query = db.query(DocumentVersion)
    
    if filters:
        if filters.get("document_id"):
            query = query.filter(DocumentVersion.document_id == filters["document_id"])
        if filters.get("version_number"):
            query = query.filter(DocumentVersion.version_number == filters["version_number"])
        if filters.get("created_by"):
            query = query.filter(DocumentVersion.created_by == filters["created_by"])
        if filters.get("created_at_from"):
            query = query.filter(DocumentVersion.created_at >= filters["created_at_from"])
        if filters.get("created_at_to"):
            query = query.filter(DocumentVersion.created_at <= filters["created_at_to"])
    
    return query.offset(skip).limit(limit).all()

def delete_version(db: Session, version_id: int) -> bool:
    db_version = get_version(db, version_id)
    if db_version:
        db.delete(db_version)
        db.commit()
        return True
    return False

# DocumentApproval CRUD
def create_approval(
    db: Session,
    approval: DocumentApprovalCreate
) -> DocumentApproval:
    db_approval = DocumentApproval(**approval.dict())
    db.add(db_approval)
    db.commit()
    db.refresh(db_approval)
    return db_approval

def get_approval(
    db: Session,
    approval_id: int
) -> Optional[DocumentApproval]:
    return db.query(DocumentApproval).filter(DocumentApproval.id == approval_id).first()

def get_approvals(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    filters: Optional[Dict[str, Any]] = None
) -> List[DocumentApproval]:
    query = db.query(DocumentApproval)
    
    if filters:
        if filters.get("document_id"):
            query = query.filter(DocumentApproval.document_id == filters["document_id"])
        if filters.get("approver_id"):
            query = query.filter(DocumentApproval.approver_id == filters["approver_id"])
        if filters.get("status"):
            query = query.filter(DocumentApproval.status == filters["status"])
        if filters.get("created_at_from"):
            query = query.filter(DocumentApproval.created_at >= filters["created_at_from"])
        if filters.get("created_at_to"):
            query = query.filter(DocumentApproval.created_at <= filters["created_at_to"])
    
    return query.offset(skip).limit(limit).all()

def update_approval(
    db: Session,
    approval_id: int,
    approval: DocumentApprovalUpdate
) -> Optional[DocumentApproval]:
    db_approval = get_approval(db, approval_id)
    if db_approval:
        update_data = approval.dict(exclude_unset=True)
        if update_data.get("status") == "approved":
            update_data["approved_at"] = datetime.utcnow()
        for key, value in update_data.items():
            setattr(db_approval, key, value)
        db.commit()
        db.refresh(db_approval)
    return db_approval

def delete_approval(db: Session, approval_id: int) -> bool:
    db_approval = get_approval(db, approval_id)
    if db_approval:
        db.delete(db_approval)
        db.commit()
        return True
    return False 