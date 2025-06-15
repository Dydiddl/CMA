from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.api import deps
from app.core.permissions import check_permissions
from app.models.user import User
from app.crud import document as crud
from app.services.file_service import FileService
from app.schemas.document import (
    Document, DocumentCreate, DocumentUpdate,
    DocumentVersion, DocumentVersionCreate,
    DocumentApproval, DocumentApprovalCreate, DocumentApprovalUpdate,
    DocumentFilter, DocumentVersionFilter, DocumentApprovalFilter,
    DocumentSearch, DocumentSearchResult,
    DocumentTag, DocumentTagCreate,
    DocumentComment, DocumentCommentCreate, DocumentCommentUpdate,
    DocumentShare, DocumentShareCreate, DocumentShareUpdate,
    DocumentStatistics
)

router = APIRouter()
file_service = FileService()

# Document 엔드포인트
@router.post("/", response_model=Document)
async def create_document(
    *,
    db: Session = Depends(deps.get_db),
    document_in: DocumentCreate,
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_user)
) -> Document:
    """
    새로운 문서를 생성합니다.
    """
    if not check_permissions(current_user, ["create:document"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="문서 생성 권한이 없습니다"
        )
    
    # 파일 저장 로직 구현 필요
    file_path = f"uploads/documents/{document_in.project_id}/{file.filename}"
    
    document = crud.create_document(
        db=db,
        document=document_in,
        user_id=current_user.id
    )
    return document

@router.get("/{document_id}", response_model=Document)
def read_document(
    *,
    db: Session = Depends(deps.get_db),
    document_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> Document:
    """
    ID로 문서를 조회합니다.
    """
    if not check_permissions(current_user, ["read:document"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="문서 조회 권한이 없습니다"
        )
    
    document = crud.get_document(db=db, document_id=document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="문서를 찾을 수 없습니다"
        )
    return document

@router.get("/", response_model=List[Document])
def read_documents(
    *,
    db: Session = Depends(deps.get_db),
    project_id: Optional[int] = None,
    document_type: Optional[str] = None,
    status: Optional[str] = None,
    created_by: Optional[int] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> List[Document]:
    """
    문서 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:document"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="문서 조회 권한이 없습니다"
        )
    
    documents = crud.get_documents(
        db=db,
        project_id=project_id,
        document_type=document_type,
        status=status,
        created_by=created_by,
        tag=tag,
        search=search,
        skip=skip,
        limit=limit
    )
    return documents

@router.put("/{document_id}", response_model=Document)
def update_document(
    *,
    db: Session = Depends(deps.get_db),
    document_id: int,
    document_in: DocumentUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> Document:
    """
    문서를 업데이트합니다.
    """
    if not check_permissions(current_user, ["update:document"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="문서 수정 권한이 없습니다"
        )
    
    document = crud.get_document(db=db, document_id=document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="문서를 찾을 수 없습니다"
        )
    
    document = crud.update_document(db=db, document_id=document_id, document=document_in)
    return document

@router.delete("/{document_id}")
def delete_document(
    *,
    db: Session = Depends(deps.get_db),
    document_id: int,
    current_user: User = Depends(deps.get_current_user)
):
    """
    문서를 삭제합니다.
    """
    if not check_permissions(current_user, ["delete:document"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="문서 삭제 권한이 없습니다"
        )
    
    document = crud.get_document(db=db, document_id=document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="문서를 찾을 수 없습니다"
        )
    
    crud.delete_document(db=db, document_id=document_id)
    return {"status": "success"}

# DocumentVersion 엔드포인트
@router.post("/{document_id}/versions", response_model=DocumentVersion)
async def create_document_version(
    *,
    db: Session = Depends(deps.get_db),
    document_id: int,
    file: UploadFile = File(...),
    changes: Optional[str] = None,
    current_user: User = Depends(deps.get_current_user)
) -> DocumentVersion:
    """
    문서의 새 버전을 생성합니다.
    """
    if not check_permissions(current_user, ["create:document_version"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="문서 버전 생성 권한이 없습니다"
        )
    
    document = crud.get_document(db=db, document_id=document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="문서를 찾을 수 없습니다"
        )
    
    # 파일 저장 로직 구현 필요
    file_path = f"uploads/documents/{document.project_id}/versions/{file.filename}"
    
    version_in = DocumentVersionCreate(
        version_number=document.version + 1,
        file_path=file_path,
        file_name=file.filename,
        file_type=file.content_type,
        file_size=file.size,
        changes=changes
    )
    
    version = crud.create_document_version(
        db=db,
        document_id=document_id,
        version=version_in,
        user_id=current_user.id
    )
    return version

@router.get("/{document_id}/versions", response_model=List[DocumentVersion])
def read_document_versions(
    *,
    db: Session = Depends(deps.get_db),
    document_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> List[DocumentVersion]:
    """
    문서의 버전 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:document_version"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="문서 버전 조회 권한이 없습니다"
        )
    
    versions = crud.get_document_versions(db=db, document_id=document_id, skip=skip, limit=limit)
    return versions

# DocumentApproval 엔드포인트
@router.post("/{document_id}/approvals", response_model=DocumentApproval)
def create_approval(
    *,
    db: Session = Depends(deps.get_db),
    document_id: int,
    approval_in: DocumentApprovalCreate,
    current_user: User = Depends(deps.get_current_user)
) -> DocumentApproval:
    """
    새로운 문서 승인 요청을 생성합니다.
    """
    if not check_permissions(current_user, ["create:document_approval"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="문서 승인 요청 생성 권한이 없습니다"
        )
    
    document = crud.get_document(db=db, document_id=document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="문서를 찾을 수 없습니다"
        )
    
    approval = crud.create_approval(db=db, approval=approval_in)
    return approval

@router.get("/{document_id}/approvals", response_model=List[DocumentApproval])
def read_approvals(
    *,
    db: Session = Depends(deps.get_db),
    document_id: int,
    skip: int = 0,
    limit: int = 100,
    approver_id: Optional[int] = None,
    status: Optional[str] = None,
    created_at_from: Optional[str] = None,
    created_at_to: Optional[str] = None,
    current_user: User = Depends(deps.get_current_user)
) -> List[DocumentApproval]:
    """
    문서 승인 요청 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:document_approval"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="문서 승인 요청 조회 권한이 없습니다"
        )
    
    filters = DocumentApprovalFilter(
        document_id=document_id,
        approver_id=approver_id,
        status=status,
        created_at_from=created_at_from,
        created_at_to=created_at_to
    )
    approvals = crud.get_approvals(
        db=db,
        skip=skip,
        limit=limit,
        filters=filters.dict(exclude_none=True)
    )
    return approvals

@router.put("/approvals/{approval_id}", response_model=DocumentApproval)
def update_approval(
    *,
    db: Session = Depends(deps.get_db),
    approval_id: int,
    approval_in: DocumentApprovalUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> DocumentApproval:
    """
    문서 승인 요청을 업데이트합니다.
    """
    if not check_permissions(current_user, ["update:document_approval"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="문서 승인 요청 수정 권한이 없습니다"
        )
    
    approval = crud.get_approval(db=db, approval_id=approval_id)
    if not approval:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="문서 승인 요청을 찾을 수 없습니다"
        )
    
    approval = crud.update_approval(
        db=db,
        approval_id=approval_id,
        approval=approval_in
    )
    return approval

@router.delete("/approvals/{approval_id}")
def delete_approval(
    *,
    db: Session = Depends(deps.get_db),
    approval_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> dict:
    """
    문서 승인 요청을 삭제합니다.
    """
    if not check_permissions(current_user, ["delete:document_approval"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="문서 승인 요청 삭제 권한이 없습니다"
        )
    
    approval = crud.get_approval(db=db, approval_id=approval_id)
    if not approval:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="문서 승인 요청을 찾을 수 없습니다"
        )
    
    crud.delete_approval(db=db, approval_id=approval_id)
    return {"status": "success"}

# Document 검색 및 필터링
@router.post("/search", response_model=List[DocumentSearchResult])
def search_documents(
    *,
    db: Session = Depends(deps.get_db),
    search: DocumentSearch,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> List[DocumentSearchResult]:
    """
    문서를 검색합니다.
    """
    if not check_permissions(current_user, ["read:document"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="문서 검색 권한이 없습니다"
        )
    
    results = crud.search_documents(
        db=db,
        search=search,
        skip=skip,
        limit=limit
    )
    return results

@router.get("/filter", response_model=List[Document])
def filter_documents(
    *,
    db: Session = Depends(deps.get_db),
    document_type: Optional[str] = None,
    status: Optional[str] = None,
    department_id: Optional[int] = None,
    created_by: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> List[Document]:
    """
    문서를 필터링합니다.
    """
    if not check_permissions(current_user, ["read:document"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="문서 필터링 권한이 없습니다"
        )
    
    filters = DocumentFilter(
        document_type=document_type,
        status=status,
        department_id=department_id,
        created_by=created_by,
        start_date=start_date,
        end_date=end_date
    )
    
    documents = crud.filter_documents(
        db=db,
        filters=filters.dict(exclude_none=True),
        skip=skip,
        limit=limit
    )
    return documents

# Document 통계
@router.get("/statistics/{project_id}", response_model=DocumentStatistics)
def read_document_statistics(
    *,
    db: Session = Depends(deps.get_db),
    project_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> DocumentStatistics:
    """
    프로젝트의 문서 통계를 조회합니다.
    """
    if not check_permissions(current_user, ["read:document_statistics"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="문서 통계 조회 권한이 없습니다"
        )
    
    statistics = crud.get_document_statistics(db=db, project_id=project_id)
    return statistics 