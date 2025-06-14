from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc

from app.models.api_doc import APIDoc, APIDocVersion, APIDocTag, APIDocComment, APIDocStatus
from app.schemas.api_doc import APIDocCreate, APIDocUpdate, APIDocVersionCreate, APIDocTagCreate, APIDocCommentCreate, APIDocCommentUpdate

def create_api_doc(db: Session, api_doc: APIDocCreate, user_id: int) -> APIDoc:
    """API 문서 생성"""
    # 태그 처리
    tags = []
    for tag_name in api_doc.tags:
        tag = db.query(APIDocTag).filter(APIDocTag.name == tag_name).first()
        if not tag:
            tag = APIDocTag(name=tag_name, created_by=user_id)
            db.add(tag)
        tags.append(tag)

    # API 문서 생성
    db_api_doc = APIDoc(
        **api_doc.dict(),
        created_by=user_id,
        updated_by=user_id,
        tags=tags
    )
    db.add(db_api_doc)
    db.commit()
    db.refresh(db_api_doc)
    return db_api_doc

def get_api_doc(db: Session, api_doc_id: int) -> Optional[APIDoc]:
    """API 문서 조회"""
    return db.query(APIDoc).filter(APIDoc.id == api_doc_id).first()

def get_api_docs(
    db: Session,
    title: Optional[str] = None,
    doc_type: Optional[str] = None,
    status: Optional[APIDocStatus] = None,
    version: Optional[str] = None,
    endpoint: Optional[str] = None,
    method: Optional[str] = None,
    created_by: Optional[int] = None,
    created_at_from: Optional[datetime] = None,
    created_at_to: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100
) -> List[APIDoc]:
    """API 문서 목록 조회"""
    query = db.query(APIDoc)
    
    if title:
        query = query.filter(APIDoc.title.ilike(f"%{title}%"))
    if doc_type:
        query = query.filter(APIDoc.doc_type == doc_type)
    if status:
        query = query.filter(APIDoc.status == status)
    if version:
        query = query.filter(APIDoc.version == version)
    if endpoint:
        query = query.filter(APIDoc.endpoint.ilike(f"%{endpoint}%"))
    if method:
        query = query.filter(APIDoc.method == method)
    if created_by:
        query = query.filter(APIDoc.created_by == created_by)
    if created_at_from:
        query = query.filter(APIDoc.created_at >= created_at_from)
    if created_at_to:
        query = query.filter(APIDoc.created_at <= created_at_to)
    
    return query.order_by(desc(APIDoc.updated_at)).offset(skip).limit(limit).all()

def update_api_doc(db: Session, api_doc_id: int, api_doc: APIDocUpdate, user_id: int) -> Optional[APIDoc]:
    """API 문서 수정"""
    db_api_doc = get_api_doc(db, api_doc_id)
    if not db_api_doc:
        return None

    # 태그 처리
    if api_doc.tags is not None:
        tags = []
        for tag_name in api_doc.tags:
            tag = db.query(APIDocTag).filter(APIDocTag.name == tag_name).first()
            if not tag:
                tag = APIDocTag(name=tag_name, created_by=user_id)
                db.add(tag)
            tags.append(tag)
        db_api_doc.tags = tags

    # 필드 업데이트
    update_data = api_doc.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field != "tags":
            setattr(db_api_doc, field, value)
    
    db_api_doc.updated_by = user_id
    db_api_doc.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_api_doc)
    return db_api_doc

def delete_api_doc(db: Session, api_doc_id: int) -> bool:
    """API 문서 삭제"""
    db_api_doc = get_api_doc(db, api_doc_id)
    if not db_api_doc:
        return False
    
    db.delete(db_api_doc)
    db.commit()
    return True

# 버전 관리
def create_api_doc_version(db: Session, api_doc_id: int, version: APIDocVersionCreate, user_id: int) -> APIDocVersion:
    """API 문서 버전 생성"""
    db_version = APIDocVersion(**version.dict(), api_doc_id=api_doc_id, created_by=user_id)
    db.add(db_version)
    db.commit()
    db.refresh(db_version)
    return db_version

def get_api_doc_version(db: Session, version_id: int) -> Optional[APIDocVersion]:
    return db.query(APIDocVersion).filter(APIDocVersion.id == version_id).first()

def get_api_doc_versions(db: Session, api_doc_id: int, skip: int = 0, limit: int = 100) -> List[APIDocVersion]:
    """API 문서 버전 목록 조회"""
    return db.query(APIDocVersion)\
        .filter(APIDocVersion.api_doc_id == api_doc_id)\
        .order_by(desc(APIDocVersion.created_at))\
        .offset(skip)\
        .limit(limit)\
        .all()

# 태그 관리
def create_api_doc_tag(db: Session, api_doc_id: int, tag: APIDocTagCreate, user_id: int) -> APIDocTag:
    db_tag = APIDocTag(**tag.dict(), api_doc_id=api_doc_id, created_by=user_id)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def get_api_doc_tags(db: Session, api_doc_id: int) -> List[APIDocTag]:
    return db.query(APIDocTag).filter(APIDocTag.api_doc_id == api_doc_id).all()

def delete_api_doc_tag(db: Session, tag_id: int) -> bool:
    db_tag = db.query(APIDocTag).filter(APIDocTag.id == tag_id).first()
    if not db_tag:
        return False
        
    db.delete(db_tag)
    db.commit()
    return True

# 댓글 관리
def create_api_doc_comment(db: Session, api_doc_id: int, comment: APIDocCommentCreate, user_id: int) -> APIDocComment:
    """API 문서 댓글 생성"""
    db_comment = APIDocComment(**comment.dict(), api_doc_id=api_doc_id, created_by=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_api_doc_comment(db: Session, comment_id: int) -> Optional[APIDocComment]:
    return db.query(APIDocComment).filter(APIDocComment.id == comment_id).first()

def get_api_doc_comments(db: Session, api_doc_id: int, skip: int = 0, limit: int = 100) -> List[APIDocComment]:
    """API 문서 댓글 목록 조회"""
    return db.query(APIDocComment)\
        .filter(APIDocComment.api_doc_id == api_doc_id)\
        .order_by(APIDocComment.created_at)\
        .offset(skip)\
        .limit(limit)\
        .all()

def update_api_doc_comment(db: Session, comment_id: int, comment: APIDocCommentUpdate) -> Optional[APIDocComment]:
    """API 문서 댓글 수정"""
    db_comment = get_api_doc_comment(db, comment_id)
    if not db_comment:
        return None
        
    update_data = comment.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_comment, field, value)
    
    db_comment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_comment)
    return db_comment

def delete_api_doc_comment(db: Session, comment_id: int) -> bool:
    """API 문서 댓글 삭제"""
    db_comment = get_api_doc_comment(db, comment_id)
    if not db_comment:
        return False
        
    db.delete(db_comment)
    db.commit()
    return True

# 통계
def get_api_doc_statistics(db: Session) -> Dict[str, Any]:
    """API 문서 통계 정보 조회"""
    # 전체 문서 수
    total_docs = db.query(func.count(APIDoc.id)).scalar()
    
    # 문서 타입별 분포
    docs_by_type = dict(
        db.query(APIDoc.doc_type, func.count(APIDoc.id))
        .group_by(APIDoc.doc_type)
        .all()
    )
    
    # 상태별 분포
    docs_by_status = dict(
        db.query(APIDoc.status, func.count(APIDoc.id))
        .group_by(APIDoc.status)
        .all()
    )
    
    # 버전별 분포
    docs_by_version = dict(
        db.query(APIDoc.version, func.count(APIDoc.id))
        .group_by(APIDoc.version)
        .all()
    )
    
    # 최근 업데이트된 문서
    recent_updates = db.query(APIDoc)\
        .order_by(desc(APIDoc.updated_at))\
        .limit(5)\
        .all()
    
    # 인기 태그
    popular_tags = dict(
        db.query(APIDocTag.name, func.count(APIDocTag.id))
        .group_by(APIDocTag.name)
        .all()
    )
    
    # 활성 사용자
    active_users = dict(
        db.query(APIDoc.created_by, func.count(APIDoc.id))
        .group_by(APIDoc.created_by)
        .all()
    )
    
    return {
        "total_docs": total_docs,
        "docs_by_type": docs_by_type,
        "docs_by_status": docs_by_status,
        "docs_by_version": docs_by_version,
        "recent_updates": [
            {
                "id": doc.id,
                "title": doc.title,
                "status": doc.status,
                "updated_at": doc.updated_at
            }
            for doc in recent_updates
        ],
        "popular_tags": popular_tags,
        "active_users": active_users
    } 