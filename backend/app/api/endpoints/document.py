from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.api import deps
from app.crud import document as crud
from app.services.file_service import FileService
from app.schemas.document import (
    Document, DocumentCreate, DocumentUpdate,
    DocumentVersion, DocumentVersionCreate,
    DocumentApproval, DocumentApprovalCreate, DocumentApprovalUpdate,
    DocumentFilter, DocumentVersionFilter, DocumentApprovalFilter,
    DocumentSearch, DocumentSearchResult
)

router = APIRouter()
file_service = FileService()

# Document 엔드포인트
@router.post("/", response_model=Document)
async def create_document(
    *,
    db: Session = Depends(deps.get_db),
    document_in: DocumentCreate = Depends(),
    file: Optional[UploadFile] = File(None),
    current_user: int = Depends(deps.get_current_user)
) -> Document:
    """
    새로운 문서를 생성합니다.
    """
    # 파일이 있는 경우 저장
    if file:
        file_url, file_name, file_size = await file_service.save_file(
            file=file,
            document_type=document_in.document_type,
            document_id=0  # 임시 ID
        )
        document_in.file_url = file_url
        document_in.file_name = file_name
        document_in.file_size = file_size
        document_in.file_type = file.content_type

    document = crud.create_document(
        db=db,
        document=document_in,
        created_by=current_user
    )
    return document

@router.get("/{document_id}", response_model=Document)
def get_document(
    *,
    db: Session = Depends(deps.get_db),
    document_id: int
) -> Document:
    """
    ID로 문서를 조회합니다.
    """
    document = crud.get_document(db=db, document_id=document_id)
    if not document:
        raise HTTPException(status_code=404, detail="문서를 찾을 수 없습니다")
    return document

@router.get("/", response_model=List[Document])
def get_documents(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    document_number: Optional[str] = None,
    title: Optional[str] = None,
    document_type: Optional[str] = None,
    status: Optional[str] = None,
    construction_id: Optional[int] = None,
    contract_id: Optional[int] = None,
    department_id: Optional[int] = None,
    created_by: Optional[int] = None,
    created_at_from: Optional[str] = None,
    created_at_to: Optional[str] = None
) -> List[Document]:
    """
    문서 목록을 조회합니다.
    """
    filters = DocumentFilter(
        document_number=document_number,
        title=title,
        document_type=document_type,
        status=status,
        construction_id=construction_id,
        contract_id=contract_id,
        department_id=department_id,
        created_by=created_by,
        created_at_from=created_at_from,
        created_at_to=created_at_to
    )
    documents = crud.get_documents(
        db=db,
        skip=skip,
        limit=limit,
        filters=filters.dict(exclude_none=True)
    )
    return documents

@router.put("/{document_id}", response_model=Document)
async def update_document(
    *,
    db: Session = Depends(deps.get_db),
    document_id: int,
    document_in: DocumentUpdate = Depends(),
    file: Optional[UploadFile] = File(None),
    current_user: int = Depends(deps.get_current_user)
) -> Document:
    """
    문서를 업데이트합니다.
    """
    document = crud.get_document(db=db, document_id=document_id)
    if not document:
        raise HTTPException(status_code=404, detail="문서를 찾을 수 없습니다")

    # 파일이 있는 경우 저장
    if file:
        # 기존 파일 삭제
        if document.file_url:
            file_service.delete_file(document.file_url)
        
        # 새 파일 저장
        file_url, file_name, file_size = await file_service.save_file(
            file=file,
            document_type=document.document_type,
            document_id=document_id,
            version=document_in.version
        )
        document_in.file_url = file_url
        document_in.file_name = file_name
        document_in.file_size = file_size
        document_in.file_type = file.content_type

    document = crud.update_document(
        db=db,
        document_id=document_id,
        document=document_in,
        updated_by=current_user
    )
    return document

@router.delete("/{document_id}")
async def delete_document(
    *,
    db: Session = Depends(deps.get_db),
    document_id: int
) -> dict:
    """
    문서를 삭제합니다.
    """
    document = crud.get_document(db=db, document_id=document_id)
    if not document:
        raise HTTPException(status_code=404, detail="문서를 찾을 수 없습니다")
    
    # 파일 삭제
    if document.file_url:
        file_service.delete_file(document.file_url)
    
    crud.delete_document(db=db, document_id=document_id)
    return {"message": "문서가 삭제되었습니다"}

# DocumentVersion 엔드포인트
@router.post("/{document_id}/versions", response_model=DocumentVersion)
async def create_version(
    *,
    db: Session = Depends(deps.get_db),
    document_id: int,
    version_in: DocumentVersionCreate = Depends(),
    file: UploadFile = File(...),
    current_user: int = Depends(deps.get_current_user)
) -> DocumentVersion:
    """
    새로운 문서 버전을 생성합니다.
    """
    document = crud.get_document(db=db, document_id=document_id)
    if not document:
        raise HTTPException(status_code=404, detail="문서를 찾을 수 없습니다")

    # 파일 저장
    file_url, file_name, file_size = await file_service.save_file(
        file=file,
        document_type=document.document_type,
        document_id=document_id,
        version=version_in.version_number
    )
    version_in.file_url = file_url
    version_in.file_name = file_name
    version_in.file_size = file_size
    version_in.file_type = file.content_type

    version = crud.create_version(
        db=db,
        version=version_in,
        created_by=current_user
    )
    return version

@router.get("/{document_id}/versions", response_model=List[DocumentVersion])
def get_versions(
    *,
    db: Session = Depends(deps.get_db),
    document_id: int,
    skip: int = 0,
    limit: int = 100,
    version_number: Optional[str] = None,
    created_by: Optional[int] = None,
    created_at_from: Optional[str] = None,
    created_at_to: Optional[str] = None
) -> List[DocumentVersion]:
    """
    문서 버전 목록을 조회합니다.
    """
    filters = DocumentVersionFilter(
        document_id=document_id,
        version_number=version_number,
        created_by=created_by,
        created_at_from=created_at_from,
        created_at_to=created_at_to
    )
    versions = crud.get_versions(
        db=db,
        skip=skip,
        limit=limit,
        filters=filters.dict(exclude_none=True)
    )
    return versions

@router.delete("/versions/{version_id}")
async def delete_version(
    *,
    db: Session = Depends(deps.get_db),
    version_id: int
) -> dict:
    """
    문서 버전을 삭제합니다.
    """
    version = crud.get_version(db=db, version_id=version_id)
    if not version:
        raise HTTPException(status_code=404, detail="문서 버전을 찾을 수 없습니다")
    
    # 파일 삭제
    if version.file_url:
        file_service.delete_file(version.file_url)
    
    crud.delete_version(db=db, version_id=version_id)
    return {"message": "문서 버전이 삭제되었습니다"}

# DocumentApproval 엔드포인트
@router.post("/{document_id}/approvals", response_model=DocumentApproval)
def create_approval(
    *,
    db: Session = Depends(deps.get_db),
    document_id: int,
    approval_in: DocumentApprovalCreate
) -> DocumentApproval:
    """
    새로운 문서 승인 요청을 생성합니다.
    """
    document = crud.get_document(db=db, document_id=document_id)
    if not document:
        raise HTTPException(status_code=404, detail="문서를 찾을 수 없습니다")
    approval = crud.create_approval(db=db, approval=approval_in)
    return approval

@router.get("/{document_id}/approvals", response_model=List[DocumentApproval])
def get_approvals(
    *,
    db: Session = Depends(deps.get_db),
    document_id: int,
    skip: int = 0,
    limit: int = 100,
    approver_id: Optional[int] = None,
    status: Optional[str] = None,
    created_at_from: Optional[str] = None,
    created_at_to: Optional[str] = None
) -> List[DocumentApproval]:
    """
    문서 승인 요청 목록을 조회합니다.
    """
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
    approval_in: DocumentApprovalUpdate
) -> DocumentApproval:
    """
    문서 승인 요청을 업데이트합니다.
    """
    approval = crud.get_approval(db=db, approval_id=approval_id)
    if not approval:
        raise HTTPException(status_code=404, detail="문서 승인 요청을 찾을 수 없습니다")
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
    approval_id: int
) -> dict:
    """
    문서 승인 요청을 삭제합니다.
    """
    approval = crud.get_approval(db=db, approval_id=approval_id)
    if not approval:
        raise HTTPException(status_code=404, detail="문서 승인 요청을 찾을 수 없습니다")
    crud.delete_approval(db=db, approval_id=approval_id)
    return {"message": "문서 승인 요청이 삭제되었습니다"}

# 문서 검색 엔드포인트
@router.post("/search", response_model=List[DocumentSearchResult])
def search_documents(
    *,
    db: Session = Depends(deps.get_db),
    search: DocumentSearch,
    skip: int = 0,
    limit: int = 100,
    current_user: int = Depends(deps.get_current_user)
) -> List[DocumentSearchResult]:
    """
    문서를 검색합니다.
    """
    return crud.search_documents(
        db=db,
        search=search,
        skip=skip,
        limit=limit
    )

# 문서 필터링 엔드포인트
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
    current_user: int = Depends(deps.get_current_user)
) -> List[Document]:
    """
    문서를 필터링합니다.
    """
    filter_params = DocumentFilter(
        document_type=document_type,
        status=status,
        department_id=department_id,
        created_by=created_by,
        start_date=start_date,
        end_date=end_date
    )
    return crud.filter_documents(
        db=db,
        filter_params=filter_params,
        skip=skip,
        limit=limit
    )

# 문서 통계 엔드포인트
@router.get("/stats")
def get_document_stats(
    *,
    db: Session = Depends(deps.get_db),
    current_user: int = Depends(deps.get_current_user)
) -> dict:
    """
    문서 통계를 조회합니다.
    """
    return crud.get_document_stats(db=db)

# 문서 버전 통계 엔드포인트
@router.get("/{document_id}/version-stats")
def get_version_stats(
    *,
    db: Session = Depends(deps.get_db),
    document_id: int,
    current_user: int = Depends(deps.get_current_user)
) -> dict:
    """
    문서 버전 통계를 조회합니다.
    """
    return crud.get_version_stats(db=db, document_id=document_id)

# 문서 승인 통계 엔드포인트
@router.get("/{document_id}/approval-stats")
def get_approval_stats(
    *,
    db: Session = Depends(deps.get_db),
    document_id: int,
    current_user: int = Depends(deps.get_current_user)
) -> dict:
    """
    문서 승인 통계를 조회합니다.
    """
    return crud.get_approval_stats(db=db, document_id=document_id)

# 문서 공유 엔드포인트
@router.post("/{document_id}/share")
def share_document(
    *,
    db: Session = Depends(deps.get_db),
    document_id: int,
    user_ids: List[int],
    permission: str = Query(..., description="권한 레벨 (read/write/admin)"),
    current_user: int = Depends(deps.get_current_user)
) -> dict:
    """
    문서를 다른 사용자와 공유합니다.
    """
    return crud.share_document(
        db=db,
        document_id=document_id,
        user_ids=user_ids,
        permission=permission,
        shared_by=current_user
    )

# 문서 공유 해제 엔드포인트
@router.delete("/{document_id}/share/{user_id}")
def unshare_document(
    *,
    db: Session = Depends(deps.get_db),
    document_id: int,
    user_id: int,
    current_user: int = Depends(deps.get_current_user)
) -> dict:
    """
    문서 공유를 해제합니다.
    """
    return crud.unshare_document(
        db=db,
        document_id=document_id,
        user_id=user_id,
        current_user=current_user
    )

# 문서 권한 변경 엔드포인트
@router.put("/{document_id}/permission/{user_id}")
def update_document_permission(
    *,
    db: Session = Depends(deps.get_db),
    document_id: int,
    user_id: int,
    permission: str = Query(..., description="새로운 권한 레벨 (read/write/admin)"),
    current_user: int = Depends(deps.get_current_user)
) -> dict:
    """
    문서 공유 권한을 변경합니다.
    """
    return crud.update_document_permission(
        db=db,
        document_id=document_id,
        user_id=user_id,
        permission=permission,
        current_user=current_user
    )

# 공유된 문서 목록 조회 엔드포인트
@router.get("/shared", response_model=List[Document])
def get_shared_documents(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: int = Depends(deps.get_current_user)
) -> List[Document]:
    """
    현재 사용자와 공유된 문서 목록을 조회합니다.
    """
    return crud.get_shared_documents(
        db=db,
        user_id=current_user,
        skip=skip,
        limit=limit
    )

# 문서 공유자 목록 조회 엔드포인트
@router.get("/{document_id}/shares")
def get_document_shares(
    *,
    db: Session = Depends(deps.get_db),
    document_id: int,
    current_user: int = Depends(deps.get_current_user)
) -> List[dict]:
    """
    문서와 공유된 사용자 목록을 조회합니다.
    """
    return crud.get_document_shares(
        db=db,
        document_id=document_id,
        current_user=current_user
    )

# 문서 알림 설정 엔드포인트
@router.post("/{document_id}/notifications")
def set_document_notification(
    *,
    db: Session = Depends(deps.get_db),
    document_id: int,
    notification_type: str = Query(..., description="알림 유형 (update/approval/comment)"),
    is_enabled: bool = True,
    current_user: int = Depends(deps.get_current_user)
) -> dict:
    """
    문서 알림을 설정합니다.
    """
    return crud.set_document_notification(
        db=db,
        document_id=document_id,
        user_id=current_user,
        notification_type=notification_type,
        is_enabled=is_enabled
    )

# 문서 알림 목록 조회 엔드포인트
@router.get("/notifications", response_model=List[dict])
def get_document_notifications(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    is_read: Optional[bool] = None,
    current_user: int = Depends(deps.get_current_user)
) -> List[dict]:
    """
    사용자의 문서 알림 목록을 조회합니다.
    """
    return crud.get_document_notifications(
        db=db,
        user_id=current_user,
        skip=skip,
        limit=limit,
        is_read=is_read
    )

# 문서 알림 읽음 처리 엔드포인트
@router.put("/notifications/{notification_id}/read")
def mark_notification_as_read(
    *,
    db: Session = Depends(deps.get_db),
    notification_id: int,
    current_user: int = Depends(deps.get_current_user)
) -> dict:
    """
    문서 알림을 읽음 처리합니다.
    """
    return crud.mark_notification_as_read(
        db=db,
        notification_id=notification_id,
        user_id=current_user
    )

# 문서 알림 일괄 읽음 처리 엔드포인트
@router.put("/notifications/read-all")
def mark_all_notifications_as_read(
    *,
    db: Session = Depends(deps.get_db),
    current_user: int = Depends(deps.get_current_user)
) -> dict:
    """
    모든 문서 알림을 읽음 처리합니다.
    """
    return crud.mark_all_notifications_as_read(
        db=db,
        user_id=current_user
    )

# 문서 알림 삭제 엔드포인트
@router.delete("/notifications/{notification_id}")
def delete_notification(
    *,
    db: Session = Depends(deps.get_db),
    notification_id: int,
    current_user: int = Depends(deps.get_current_user)
) -> dict:
    """
    문서 알림을 삭제합니다.
    """
    return crud.delete_notification(
        db=db,
        notification_id=notification_id,
        user_id=current_user
    )

# 문서 댓글 생성 엔드포인트
@router.post("/{document_id}/comments")
def create_document_comment(
    *,
    db: Session = Depends(deps.get_db),
    document_id: int,
    content: str = Form(...),
    parent_id: Optional[int] = None,
    current_user: int = Depends(deps.get_current_user)
) -> dict:
    """
    문서에 댓글을 작성합니다.
    """
    return crud.create_document_comment(
        db=db,
        document_id=document_id,
        user_id=current_user,
        content=content,
        parent_id=parent_id
    )

# 문서 댓글 목록 조회 엔드포인트
@router.get("/{document_id}/comments")
def get_document_comments(
    *,
    db: Session = Depends(deps.get_db),
    document_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: int = Depends(deps.get_current_user)
) -> List[dict]:
    """
    문서의 댓글 목록을 조회합니다.
    """
    return crud.get_document_comments(
        db=db,
        document_id=document_id,
        skip=skip,
        limit=limit
    )

# 문서 댓글 수정 엔드포인트
@router.put("/comments/{comment_id}")
def update_document_comment(
    *,
    db: Session = Depends(deps.get_db),
    comment_id: int,
    content: str = Form(...),
    current_user: int = Depends(deps.get_current_user)
) -> dict:
    """
    문서 댓글을 수정합니다.
    """
    return crud.update_document_comment(
        db=db,
        comment_id=comment_id,
        content=content,
        user_id=current_user
    )

# 문서 댓글 삭제 엔드포인트
@router.delete("/comments/{comment_id}")
def delete_document_comment(
    *,
    db: Session = Depends(deps.get_db),
    comment_id: int,
    current_user: int = Depends(deps.get_current_user)
) -> dict:
    """
    문서 댓글을 삭제합니다.
    """
    return crud.delete_document_comment(
        db=db,
        comment_id=comment_id,
        user_id=current_user
    )

# 문서 댓글 좋아요/싫어요 엔드포인트
@router.post("/comments/{comment_id}/reaction")
def react_to_comment(
    *,
    db: Session = Depends(deps.get_db),
    comment_id: int,
    reaction_type: str = Query(..., description="반응 유형 (like/dislike)"),
    current_user: int = Depends(deps.get_current_user)
) -> dict:
    """
    문서 댓글에 좋아요/싫어요를 표시합니다.
    """
    return crud.react_to_comment(
        db=db,
        comment_id=comment_id,
        user_id=current_user,
        reaction_type=reaction_type
    ) 