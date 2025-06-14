from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import api_doc as crud
from app.schemas.api_doc import (
    ApiDoc,
    ApiDocCreate,
    ApiDocUpdate,
    ApiDocVersion,
    ApiDocVersionCreate,
    ApiDocComment,
    ApiDocCommentCreate,
    ApiDocCommentUpdate,
    ApiDocStatistics,
    ApiDocResponse,
    ApiDocVersionResponse,
    ApiDocCommentResponse
)

router = APIRouter()

@router.post("/", response_model=ApiDoc)
def create_api_doc(
    *,
    db: Session = Depends(deps.get_db),
    doc_in: ApiDocCreate,
    current_user = Depends(deps.get_current_active_user)
) -> ApiDoc:
    """API 문서 생성"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="API 문서를 생성할 권한이 없습니다."
        )
    return crud.create_api_doc(db, doc_in, current_user.id)

@router.get("/{doc_id}", response_model=ApiDoc)
def read_api_doc(
    *,
    db: Session = Depends(deps.get_db),
    doc_id: int,
    current_user = Depends(deps.get_current_active_user)
) -> ApiDoc:
    """API 문서 조회"""
    doc = crud.get_api_doc(db, doc_id)
    if not doc:
        raise HTTPException(
            status_code=404,
            detail="API 문서를 찾을 수 없습니다."
        )
    return doc

@router.get("/", response_model=ApiDocResponse)
def read_api_docs(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    current_user = Depends(deps.get_current_active_user)
) -> ApiDocResponse:
    """API 문서 목록 조회"""
    docs = crud.get_api_docs(
        db,
        skip=skip,
        limit=limit,
        category=category,
        status=status,
        search=search
    )
    total = len(docs)  # 실제로는 전체 개수를 별도로 조회해야 함
    return {"items": docs, "total": total}

@router.put("/{doc_id}", response_model=ApiDoc)
def update_api_doc(
    *,
    db: Session = Depends(deps.get_db),
    doc_id: int,
    doc_in: ApiDocUpdate,
    current_user = Depends(deps.get_current_active_user)
) -> ApiDoc:
    """API 문서 수정"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="API 문서를 수정할 권한이 없습니다."
        )
    doc = crud.update_api_doc(db, doc_id, doc_in, current_user.id)
    if not doc:
        raise HTTPException(
            status_code=404,
            detail="API 문서를 찾을 수 없습니다."
        )
    return doc

@router.delete("/{doc_id}")
def delete_api_doc(
    *,
    db: Session = Depends(deps.get_db),
    doc_id: int,
    current_user = Depends(deps.get_current_active_user)
):
    """API 문서 삭제"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="API 문서를 삭제할 권한이 없습니다."
        )
    if not crud.delete_api_doc(db, doc_id):
        raise HTTPException(
            status_code=404,
            detail="API 문서를 찾을 수 없습니다."
        )
    return {"message": "API 문서가 삭제되었습니다."}

@router.post("/{doc_id}/versions", response_model=ApiDocVersion)
def create_api_doc_version(
    *,
    db: Session = Depends(deps.get_db),
    doc_id: int,
    version_in: ApiDocVersionCreate,
    current_user = Depends(deps.get_current_active_user)
) -> ApiDocVersion:
    """API 문서 버전 생성"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="API 문서 버전을 생성할 권한이 없습니다."
        )
    version = crud.create_api_doc_version(db, doc_id, version_in, current_user.id)
    if not version:
        raise HTTPException(
            status_code=404,
            detail="API 문서를 찾을 수 없습니다."
        )
    return version

@router.get("/{doc_id}/versions", response_model=ApiDocVersionResponse)
def read_api_doc_versions(
    *,
    db: Session = Depends(deps.get_db),
    doc_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(deps.get_current_active_user)
) -> ApiDocVersionResponse:
    """API 문서 버전 목록 조회"""
    versions = crud.get_api_doc_versions(db, doc_id, skip=skip, limit=limit)
    total = len(versions)  # 실제로는 전체 개수를 별도로 조회해야 함
    return {"items": versions, "total": total}

@router.post("/{doc_id}/tags")
def add_api_doc_tags(
    *,
    db: Session = Depends(deps.get_db),
    doc_id: int,
    tags: List[str],
    current_user = Depends(deps.get_current_active_user)
):
    """API 문서에 태그 추가"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="API 문서에 태그를 추가할 권한이 없습니다."
        )
    doc = crud.add_api_doc_tags(db, doc_id, tags, current_user.id)
    if not doc:
        raise HTTPException(
            status_code=404,
            detail="API 문서를 찾을 수 없습니다."
        )
    return {"message": "태그가 추가되었습니다."}

@router.post("/{doc_id}/comments", response_model=ApiDocComment)
def create_api_doc_comment(
    *,
    db: Session = Depends(deps.get_db),
    doc_id: int,
    comment_in: ApiDocCommentCreate,
    current_user = Depends(deps.get_current_active_user)
) -> ApiDocComment:
    """API 문서 댓글 생성"""
    comment = crud.create_api_doc_comment(db, doc_id, comment_in, current_user.id)
    if not comment:
        raise HTTPException(
            status_code=404,
            detail="API 문서를 찾을 수 없습니다."
        )
    return comment

@router.get("/{doc_id}/comments", response_model=ApiDocCommentResponse)
def read_api_doc_comments(
    *,
    db: Session = Depends(deps.get_db),
    doc_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(deps.get_current_active_user)
) -> ApiDocCommentResponse:
    """API 문서 댓글 목록 조회"""
    comments = crud.get_api_doc_comments(db, doc_id, skip=skip, limit=limit)
    total = len(comments)  # 실제로는 전체 개수를 별도로 조회해야 함
    return {"items": comments, "total": total}

@router.put("/comments/{comment_id}", response_model=ApiDocComment)
def update_api_doc_comment(
    *,
    db: Session = Depends(deps.get_db),
    comment_id: int,
    comment_in: ApiDocCommentUpdate,
    current_user = Depends(deps.get_current_active_user)
) -> ApiDocComment:
    """API 문서 댓글 수정"""
    comment = crud.update_api_doc_comment(db, comment_id, comment_in, current_user.id)
    if not comment:
        raise HTTPException(
            status_code=404,
            detail="댓글을 찾을 수 없습니다."
        )
    return comment

@router.delete("/comments/{comment_id}")
def delete_api_doc_comment(
    *,
    db: Session = Depends(deps.get_db),
    comment_id: int,
    current_user = Depends(deps.get_current_active_user)
):
    """API 문서 댓글 삭제"""
    if not crud.delete_api_doc_comment(db, comment_id):
        raise HTTPException(
            status_code=404,
            detail="댓글을 찾을 수 없습니다."
        )
    return {"message": "댓글이 삭제되었습니다."}

@router.get("/statistics", response_model=ApiDocStatistics)
def get_api_doc_statistics(
    *,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
) -> ApiDocStatistics:
    """API 문서 통계 정보 조회"""
    return crud.get_api_doc_statistics(db) 