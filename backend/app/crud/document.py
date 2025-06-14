from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime

from app.models.document import Document, DocumentVersion, DocumentTag, DocumentComment, DocumentShare, DocumentStatus
from app.schemas.document import (
    DocumentCreate, DocumentUpdate,
    DocumentVersionCreate, DocumentVersionUpdate,
    DocumentTagCreate, DocumentCommentCreate, DocumentCommentUpdate,
    DocumentShareCreate, DocumentShareUpdate
)

# Document CRUD
def create_document(db: Session, document: DocumentCreate, user_id: int) -> Document:
    db_document = Document(
        **document.dict(),
        status=DocumentStatus.DRAFT,
        version=1,
        created_by=user_id
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_document(db: Session, document_id: int) -> Optional[Document]:
    return db.query(Document).filter(Document.id == document_id).first()

def get_documents(
    db: Session,
    project_id: Optional[int] = None,
    document_type: Optional[str] = None,
    status: Optional[DocumentStatus] = None,
    created_by: Optional[int] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Document]:
    query = db.query(Document)
    
    if project_id:
        query = query.filter(Document.project_id == project_id)
    if document_type:
        query = query.filter(Document.document_type == document_type)
    if status:
        query = query.filter(Document.status == status)
    if created_by:
        query = query.filter(Document.created_by == created_by)
    if tag:
        query = query.join(DocumentTag).filter(DocumentTag.name == tag)
    if search:
        search_filter = or_(
            Document.title.ilike(f"%{search}%"),
            Document.description.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
        
    return query.offset(skip).limit(limit).all()

def update_document(db: Session, document_id: int, document: DocumentUpdate) -> Optional[Document]:
    db_document = get_document(db, document_id)
    if not db_document:
        return None
        
    update_data = document.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_document, field, value)
    
    db_document.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_document)
    return db_document

def delete_document(db: Session, document_id: int) -> bool:
    db_document = get_document(db, document_id)
    if not db_document:
        return False
        
    db.delete(db_document)
    db.commit()
    return True

# DocumentVersion CRUD
def create_document_version(db: Session, document_id: int, version: DocumentVersionCreate, user_id: int) -> DocumentVersion:
    db_version = DocumentVersion(**version.dict(), document_id=document_id, created_by=user_id)
    db.add(db_version)
    
    # 문서 버전 업데이트
    db_document = get_document(db, document_id)
    if db_document:
        db_document.version = version.version_number
        db_document.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_version)
    return db_version

def get_document_version(db: Session, version_id: int) -> Optional[DocumentVersion]:
    return db.query(DocumentVersion).filter(DocumentVersion.id == version_id).first()

def get_document_versions(db: Session, document_id: int, skip: int = 0, limit: int = 100) -> List[DocumentVersion]:
    return db.query(DocumentVersion).filter(DocumentVersion.document_id == document_id).offset(skip).limit(limit).all()

# DocumentTag CRUD
def create_document_tag(db: Session, document_id: int, tag: DocumentTagCreate, user_id: int) -> DocumentTag:
    db_tag = DocumentTag(**tag.dict(), document_id=document_id, created_by=user_id)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def get_document_tags(db: Session, document_id: int) -> List[DocumentTag]:
    return db.query(DocumentTag).filter(DocumentTag.document_id == document_id).all()

def delete_document_tag(db: Session, tag_id: int) -> bool:
    db_tag = db.query(DocumentTag).filter(DocumentTag.id == tag_id).first()
    if not db_tag:
        return False
        
    db.delete(db_tag)
    db.commit()
    return True

# DocumentComment CRUD
def create_document_comment(db: Session, document_id: int, comment: DocumentCommentCreate, user_id: int) -> DocumentComment:
    db_comment = DocumentComment(**comment.dict(), document_id=document_id, created_by=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_document_comment(db: Session, comment_id: int) -> Optional[DocumentComment]:
    return db.query(DocumentComment).filter(DocumentComment.id == comment_id).first()

def get_document_comments(db: Session, document_id: int, skip: int = 0, limit: int = 100) -> List[DocumentComment]:
    return db.query(DocumentComment).filter(DocumentComment.document_id == document_id).offset(skip).limit(limit).all()

def update_document_comment(db: Session, comment_id: int, comment: DocumentCommentUpdate) -> Optional[DocumentComment]:
    db_comment = get_document_comment(db, comment_id)
    if not db_comment:
        return None
        
    update_data = comment.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_comment, field, value)
    
    db_comment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_comment)
    return db_comment

def delete_document_comment(db: Session, comment_id: int) -> bool:
    db_comment = get_document_comment(db, comment_id)
    if not db_comment:
        return False
        
    db.delete(db_comment)
    db.commit()
    return True

# DocumentShare CRUD
def create_document_share(db: Session, document_id: int, share: DocumentShareCreate, user_id: int) -> DocumentShare:
    db_share = DocumentShare(**share.dict(), document_id=document_id, created_by=user_id)
    db.add(db_share)
    db.commit()
    db.refresh(db_share)
    return db_share

def get_document_share(db: Session, share_id: int) -> Optional[DocumentShare]:
    return db.query(DocumentShare).filter(DocumentShare.id == share_id).first()

def get_document_shares(db: Session, document_id: int, skip: int = 0, limit: int = 100) -> List[DocumentShare]:
    return db.query(DocumentShare).filter(DocumentShare.document_id == document_id).offset(skip).limit(limit).all()

def update_document_share(db: Session, share_id: int, share: DocumentShareUpdate) -> Optional[DocumentShare]:
    db_share = get_document_share(db, share_id)
    if not db_share:
        return None
        
    update_data = share.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_share, field, value)
    
    db.commit()
    db.refresh(db_share)
    return db_share

def delete_document_share(db: Session, share_id: int) -> bool:
    db_share = get_document_share(db, share_id)
    if not db_share:
        return False
        
    db.delete(db_share)
    db.commit()
    return True

# DocumentStatistics
def get_document_statistics(db: Session, project_id: int) -> Dict[str, Any]:
    # 기본 통계
    total_documents = db.query(func.count(Document.id)).filter(Document.project_id == project_id).scalar()
    total_size = db.query(func.sum(Document.file_size)).filter(Document.project_id == project_id).scalar() or 0
    
    # 문서 타입별 분포
    documents_by_type = dict(
        db.query(Document.document_type, func.count(Document.id))
        .filter(Document.project_id == project_id)
        .group_by(Document.document_type)
        .all()
    )
    
    # 상태별 분포
    documents_by_status = dict(
        db.query(Document.status, func.count(Document.id))
        .filter(Document.project_id == project_id)
        .group_by(Document.status)
        .all()
    )
    
    # 최근 업로드
    recent_uploads = db.query(Document)\
        .filter(Document.project_id == project_id)\
        .order_by(Document.created_at.desc())\
        .limit(5)\
        .all()
    
    # 인기 태그
    popular_tags = dict(
        db.query(DocumentTag.name, func.count(DocumentTag.id))
        .join(Document)
        .filter(Document.project_id == project_id)
        .group_by(DocumentTag.name)
        .all()
    )
    
    # 활성 사용자
    active_users = dict(
        db.query(Document.created_by, func.count(Document.id))
        .filter(Document.project_id == project_id)
        .group_by(Document.created_by)
        .all()
    )
    
    return {
        "total_documents": total_documents,
        "documents_by_type": documents_by_type,
        "documents_by_status": documents_by_status,
        "total_size": total_size,
        "recent_uploads": recent_uploads,
        "popular_tags": popular_tags,
        "active_users": active_users
    } 