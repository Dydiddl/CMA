from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.vendor import Vendor, VendorDocument
from ..schemas.vendor import VendorCreate, VendorUpdate, VendorDocumentCreate

def create_vendor(db: Session, vendor: VendorCreate) -> Vendor:
    """새로운 거래처를 등록합니다."""
    db_vendor = Vendor(**vendor.dict())
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor

def get_vendors(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None
) -> List[Vendor]:
    """거래처 목록을 조회합니다."""
    query = db.query(Vendor)
    if status:
        query = query.filter(Vendor.status == status)
    return query.offset(skip).limit(limit).all()

def get_vendor(db: Session, vendor_id: int) -> Optional[Vendor]:
    """특정 거래처의 정보를 조회합니다."""
    return db.query(Vendor).filter(Vendor.id == vendor_id).first()

def update_vendor(
    db: Session,
    vendor_id: int,
    vendor: VendorUpdate
) -> Optional[Vendor]:
    """거래처 정보를 업데이트합니다."""
    db_vendor = get_vendor(db, vendor_id)
    if db_vendor:
        for key, value in vendor.dict(exclude_unset=True).items():
            setattr(db_vendor, key, value)
        db.commit()
        db.refresh(db_vendor)
    return db_vendor

def delete_vendor(db: Session, vendor_id: int) -> bool:
    """거래처를 삭제합니다."""
    db_vendor = get_vendor(db, vendor_id)
    if db_vendor:
        db.delete(db_vendor)
        db.commit()
        return True
    return False

def create_vendor_document(
    db: Session,
    vendor_id: int,
    document: VendorDocumentCreate
) -> VendorDocument:
    """거래처 문서를 생성합니다."""
    db_document = VendorDocument(**document.dict(), vendor_id=vendor_id)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_vendor_documents(
    db: Session,
    vendor_id: int
) -> List[VendorDocument]:
    """거래처의 모든 문서를 조회합니다."""
    return db.query(VendorDocument).filter(
        VendorDocument.vendor_id == vendor_id
    ).all() 