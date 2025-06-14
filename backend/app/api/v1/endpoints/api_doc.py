from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.core.permissions import check_permissions
from app.models.user import User
from app.schemas.api_doc import (
    APIDocCreate, APIDocUpdate, APIDoc,
    APIDocVersion, APIDocVersionCreate,
    APIDocTag, APIDocTagCreate,
    APIDocComment, APIDocCommentCreate,
    APIDocStatistics
)
from app.crud import api_doc as api_doc_crud

router = APIRouter()

# API 문서 기본 CRUD
@router.post("/", response_model=APIDoc)
def create_api_doc(
    *,
    db: Session = Depends(deps.get_db),
    api_doc_in: APIDocCreate,
    current_user: User = Depends(deps.get_current_user)
) -> APIDoc:
    """
    새로운 API 문서를 생성합니다.
    """
    if not check_permissions(current_user, ["create:api_doc"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API 문서 생성 권한이 없습니다"
        )
    
    api_doc = api_doc_crud.create(
        db=db,
        obj_in=api_doc_in,
        creator_id=current_user.id
    )
    return api_doc

@router.get("/", response_model=List[APIDoc])
def read_api_docs(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    title: Optional[str] = None,
    doc_type: Optional[str] = None,
    status: Optional[str] = None,
    current_user: User = Depends(deps.get_current_user)
) -> List[APIDoc]:
    """
    API 문서 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:api_doc"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API 문서 조회 권한이 없습니다"
        )
    
    api_docs = api_doc_crud.get_multi(
        db=db,
        skip=skip,
        limit=limit,
        title=title,
        doc_type=doc_type,
        status=status
    )
    return api_docs

@router.get("/{api_doc_id}", response_model=APIDoc)
def read_api_doc(
    *,
    db: Session = Depends(deps.get_db),
    api_doc_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> APIDoc:
    """
    특정 API 문서를 조회합니다.
    """
    if not check_permissions(current_user, ["read:api_doc"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API 문서 조회 권한이 없습니다"
        )
    
    api_doc = api_doc_crud.get(db=db, id=api_doc_id)
    if not api_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API 문서를 찾을 수 없습니다"
        )
    return api_doc

@router.put("/{api_doc_id}", response_model=APIDoc)
def update_api_doc(
    *,
    db: Session = Depends(deps.get_db),
    api_doc_id: int,
    api_doc_in: APIDocUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> APIDoc:
    """
    API 문서를 업데이트합니다.
    """
    if not check_permissions(current_user, ["update:api_doc"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API 문서 수정 권한이 없습니다"
        )
    
    api_doc = api_doc_crud.get(db=db, id=api_doc_id)
    if not api_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API 문서를 찾을 수 없습니다"
        )
    
    api_doc = api_doc_crud.update(
        db=db,
        db_obj=api_doc,
        obj_in=api_doc_in
    )
    return api_doc

@router.delete("/{api_doc_id}")
def delete_api_doc(
    *,
    db: Session = Depends(deps.get_db),
    api_doc_id: int,
    current_user: User = Depends(deps.get_current_user)
):
    """
    API 문서를 삭제합니다.
    """
    if not check_permissions(current_user, ["delete:api_doc"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API 문서 삭제 권한이 없습니다"
        )
    
    api_doc = api_doc_crud.get(db=db, id=api_doc_id)
    if not api_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API 문서를 찾을 수 없습니다"
        )
    
    api_doc_crud.remove(db=db, id=api_doc_id)
    return {"status": "success"}

# API 문서 버전 관리
@router.post("/{api_doc_id}/versions", response_model=APIDocVersion)
def create_version(
    *,
    db: Session = Depends(deps.get_db),
    api_doc_id: int,
    version_in: APIDocVersionCreate,
    current_user: User = Depends(deps.get_current_user)
) -> APIDocVersion:
    """
    API 문서의 새 버전을 생성합니다.
    """
    if not check_permissions(current_user, ["create:api_doc_version"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API 문서 버전 생성 권한이 없습니다"
        )
    
    api_doc = api_doc_crud.get(db=db, id=api_doc_id)
    if not api_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API 문서를 찾을 수 없습니다"
        )
    
    version = api_doc_crud.create_version(
        db=db,
        api_doc_id=api_doc_id,
        version_in=version_in,
        creator_id=current_user.id
    )
    return version

# API 문서 태그 관리
@router.post("/{api_doc_id}/tags", response_model=APIDocTag)
def create_tag(
    *,
    db: Session = Depends(deps.get_db),
    api_doc_id: int,
    tag_in: APIDocTagCreate,
    current_user: User = Depends(deps.get_current_user)
) -> APIDocTag:
    """
    API 문서에 새 태그를 추가합니다.
    """
    if not check_permissions(current_user, ["create:api_doc_tag"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API 문서 태그 생성 권한이 없습니다"
        )
    
    api_doc = api_doc_crud.get(db=db, id=api_doc_id)
    if not api_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API 문서를 찾을 수 없습니다"
        )
    
    tag = api_doc_crud.create_tag(
        db=db,
        api_doc_id=api_doc_id,
        tag_in=tag_in,
        creator_id=current_user.id
    )
    return tag

# API 문서 댓글 관리
@router.post("/{api_doc_id}/comments", response_model=APIDocComment)
def create_comment(
    *,
    db: Session = Depends(deps.get_db),
    api_doc_id: int,
    comment_in: APIDocCommentCreate,
    current_user: User = Depends(deps.get_current_user)
) -> APIDocComment:
    """
    API 문서에 새 댓글을 추가합니다.
    """
    if not check_permissions(current_user, ["create:api_doc_comment"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API 문서 댓글 생성 권한이 없습니다"
        )
    
    api_doc = api_doc_crud.get(db=db, id=api_doc_id)
    if not api_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API 문서를 찾을 수 없습니다"
        )
    
    comment = api_doc_crud.create_comment(
        db=db,
        api_doc_id=api_doc_id,
        comment_in=comment_in,
        creator_id=current_user.id
    )
    return comment

# API 문서 통계
@router.get("/statistics", response_model=APIDocStatistics)
def get_statistics(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> APIDocStatistics:
    """
    API 문서 통계를 조회합니다.
    """
    if not check_permissions(current_user, ["read:api_doc_statistics"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API 문서 통계 조회 권한이 없습니다"
        )
    
    statistics = api_doc_crud.get_statistics(db=db)
    return statistics 