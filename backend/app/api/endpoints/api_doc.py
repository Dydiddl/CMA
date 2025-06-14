from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import api_doc as api_doc_crud
from app.schemas.api_doc import (
    APIDoc, APIDocCreate, APIDocUpdate,
    APIDocVersion, APIDocVersionCreate,
    APIDocTag, APIDocTagCreate,
    APIDocComment, APIDocCommentCreate, APIDocCommentUpdate,
    APIDocStatistics
)

router = APIRouter()

# API 문서 CRUD
@router.post("/", response_model=APIDoc)
def create_api_doc(
    *,
    db: Session = Depends(deps.get_db),
    api_doc_in: APIDocCreate,
    current_user = Depends(deps.get_current_user)
):
    """
    새로운 API 문서를 생성합니다.
    """
    api_doc = api_doc_crud.create_api_doc(
        db=db,
        api_doc=api_doc_in,
        user_id=current_user.id
    )
    return api_doc

@router.get("/{api_doc_id}", response_model=APIDoc)
def get_api_doc(
    *,
    db: Session = Depends(deps.get_db),
    api_doc_id: int,
    current_user = Depends(deps.get_current_user)
):
    """
    ID로 API 문서를 조회합니다.
    """
    api_doc = api_doc_crud.get_api_doc(db=db, api_doc_id=api_doc_id)
    if not api_doc:
        raise HTTPException(status_code=404, detail="API 문서를 찾을 수 없습니다")
    return api_doc

@router.get("/", response_model=List[APIDoc])
def get_api_docs(
    *,
    db: Session = Depends(deps.get_db),
    title: Optional[str] = None,
    doc_type: Optional[str] = None,
    status: Optional[str] = None,
    version: Optional[str] = None,
    endpoint: Optional[str] = None,
    method: Optional[str] = None,
    created_by: Optional[int] = None,
    created_at_from: Optional[str] = None,
    created_at_to: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(deps.get_current_user)
):
    """
    API 문서 목록을 조회합니다.
    """
    api_docs = api_doc_crud.get_api_docs(
        db=db,
        title=title,
        doc_type=doc_type,
        status=status,
        version=version,
        endpoint=endpoint,
        method=method,
        created_by=created_by,
        created_at_from=created_at_from,
        created_at_to=created_at_to,
        skip=skip,
        limit=limit
    )
    return api_docs

@router.put("/{api_doc_id}", response_model=APIDoc)
def update_api_doc(
    *,
    db: Session = Depends(deps.get_db),
    api_doc_id: int,
    api_doc_in: APIDocUpdate,
    current_user = Depends(deps.get_current_user)
):
    """
    API 문서를 업데이트합니다.
    """
    api_doc = api_doc_crud.get_api_doc(db=db, api_doc_id=api_doc_id)
    if not api_doc:
        raise HTTPException(status_code=404, detail="API 문서를 찾을 수 없습니다")
    api_doc = api_doc_crud.update_api_doc(
        db=db,
        api_doc_id=api_doc_id,
        api_doc=api_doc_in,
        user_id=current_user.id
    )
    return api_doc

@router.delete("/{api_doc_id}")
def delete_api_doc(
    *,
    db: Session = Depends(deps.get_db),
    api_doc_id: int,
    current_user = Depends(deps.get_current_user)
):
    """
    API 문서를 삭제합니다.
    """
    api_doc = api_doc_crud.get_api_doc(db=db, api_doc_id=api_doc_id)
    if not api_doc:
        raise HTTPException(status_code=404, detail="API 문서를 찾을 수 없습니다")
    api_doc_crud.delete_api_doc(db=db, api_doc_id=api_doc_id)
    return {"status": "success"}

# 버전 관리
@router.post("/{api_doc_id}/versions", response_model=APIDocVersion)
def create_api_doc_version(
    *,
    db: Session = Depends(deps.get_db),
    api_doc_id: int,
    version_in: APIDocVersionCreate,
    current_user = Depends(deps.get_current_user)
):
    """
    API 문서의 새 버전을 생성합니다.
    """
    api_doc = api_doc_crud.get_api_doc(db=db, api_doc_id=api_doc_id)
    if not api_doc:
        raise HTTPException(status_code=404, detail="API 문서를 찾을 수 없습니다")
    version = api_doc_crud.create_api_doc_version(
        db=db,
        api_doc_id=api_doc_id,
        version=version_in,
        user_id=current_user.id
    )
    return version

@router.get("/{api_doc_id}/versions", response_model=List[APIDocVersion])
def get_api_doc_versions(
    *,
    db: Session = Depends(deps.get_db),
    api_doc_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(deps.get_current_user)
):
    """
    API 문서의 버전 목록을 조회합니다.
    """
    versions = api_doc_crud.get_api_doc_versions(db=db, api_doc_id=api_doc_id, skip=skip, limit=limit)
    return versions

# 태그 관리
@router.post("/{api_doc_id}/tags", response_model=APIDocTag)
def create_api_doc_tag(
    *,
    db: Session = Depends(deps.get_db),
    api_doc_id: int,
    tag_in: APIDocTagCreate,
    current_user = Depends(deps.get_current_user)
):
    """
    API 문서에 태그를 추가합니다.
    """
    api_doc = api_doc_crud.get_api_doc(db=db, api_doc_id=api_doc_id)
    if not api_doc:
        raise HTTPException(status_code=404, detail="API 문서를 찾을 수 없습니다")
    tag = api_doc_crud.create_api_doc_tag(
        db=db,
        api_doc_id=api_doc_id,
        tag=tag_in,
        user_id=current_user.id
    )
    return tag

@router.get("/{api_doc_id}/tags", response_model=List[APIDocTag])
def get_api_doc_tags(
    *,
    db: Session = Depends(deps.get_db),
    api_doc_id: int,
    current_user = Depends(deps.get_current_user)
):
    """
    API 문서의 태그 목록을 조회합니다.
    """
    tags = api_doc_crud.get_api_doc_tags(db=db, api_doc_id=api_doc_id)
    return tags

@router.delete("/tags/{tag_id}")
def delete_api_doc_tag(
    *,
    db: Session = Depends(deps.get_db),
    tag_id: int,
    current_user = Depends(deps.get_current_user)
):
    """
    API 문서의 태그를 삭제합니다.
    """
    tag = api_doc_crud.get_api_doc_tag(db=db, tag_id=tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="태그를 찾을 수 없습니다")
    api_doc_crud.delete_api_doc_tag(db=db, tag_id=tag_id)
    return {"status": "success"}

# 댓글 관리
@router.post("/{api_doc_id}/comments", response_model=APIDocComment)
def create_api_doc_comment(
    *,
    db: Session = Depends(deps.get_db),
    api_doc_id: int,
    comment_in: APIDocCommentCreate,
    current_user = Depends(deps.get_current_user)
):
    """
    API 문서에 댓글을 추가합니다.
    """
    api_doc = api_doc_crud.get_api_doc(db=db, api_doc_id=api_doc_id)
    if not api_doc:
        raise HTTPException(status_code=404, detail="API 문서를 찾을 수 없습니다")
    comment = api_doc_crud.create_api_doc_comment(
        db=db,
        api_doc_id=api_doc_id,
        comment=comment_in,
        user_id=current_user.id
    )
    return comment

@router.get("/{api_doc_id}/comments", response_model=List[APIDocComment])
def get_api_doc_comments(
    *,
    db: Session = Depends(deps.get_db),
    api_doc_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(deps.get_current_user)
):
    """
    API 문서의 댓글 목록을 조회합니다.
    """
    comments = api_doc_crud.get_api_doc_comments(db=db, api_doc_id=api_doc_id, skip=skip, limit=limit)
    return comments

@router.put("/comments/{comment_id}", response_model=APIDocComment)
def update_api_doc_comment(
    *,
    db: Session = Depends(deps.get_db),
    comment_id: int,
    comment_in: APIDocCommentUpdate,
    current_user = Depends(deps.get_current_user)
):
    """
    API 문서의 댓글을 업데이트합니다.
    """
    comment = api_doc_crud.get_api_doc_comment(db=db, comment_id=comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다")
    comment = api_doc_crud.update_api_doc_comment(db=db, comment_id=comment_id, comment=comment_in)
    return comment

@router.delete("/comments/{comment_id}")
def delete_api_doc_comment(
    *,
    db: Session = Depends(deps.get_db),
    comment_id: int,
    current_user = Depends(deps.get_current_user)
):
    """
    API 문서의 댓글을 삭제합니다.
    """
    comment = api_doc_crud.get_api_doc_comment(db=db, comment_id=comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다")
    api_doc_crud.delete_api_doc_comment(db=db, comment_id=comment_id)
    return {"status": "success"}

# 통계
@router.get("/statistics", response_model=APIDocStatistics)
def get_api_doc_statistics(
    *,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_user)
):
    """
    API 문서 통계를 조회합니다.
    """
    statistics = api_doc_crud.get_api_doc_statistics(db=db)
    return statistics 