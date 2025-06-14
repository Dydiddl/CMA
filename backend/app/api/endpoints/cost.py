from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.api import deps
from app.crud import cost as crud
from app.schemas.cost import (
    Cost, CostCreate, CostUpdate,
    CostAttachment, CostApproval,
    CostFilter, CostStatistics
)
from app.services.file_service import FileService

router = APIRouter()
file_service = FileService()

# Cost 엔드포인트
@router.post("/", response_model=Cost)
async def create_cost(
    *,
    db: Session = Depends(deps.get_db),
    cost_in: CostCreate = Depends(),
    current_user: int = Depends(deps.get_current_user)
) -> Cost:
    """
    새로운 비용을 생성합니다.
    """
    return crud.create_cost(db=db, cost=cost_in, created_by=current_user)

@router.get("/{cost_id}", response_model=Cost)
def get_cost(
    *,
    db: Session = Depends(deps.get_db),
    cost_id: int,
    current_user: int = Depends(deps.get_current_user)
) -> Cost:
    """
    비용을 조회합니다.
    """
    cost = crud.get_cost(db=db, cost_id=cost_id)
    if not cost:
        raise HTTPException(status_code=404, detail="비용을 찾을 수 없습니다")
    return cost

@router.get("/", response_model=List[Cost])
def get_costs(
    *,
    db: Session = Depends(deps.get_db),
    project_id: Optional[int] = None,
    cost_type: Optional[str] = None,
    category: Optional[str] = None,
    payment_status: Optional[str] = None,
    vendor_id: Optional[int] = None,
    department_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: int = Depends(deps.get_current_user)
) -> List[Cost]:
    """
    비용 목록을 조회합니다.
    """
    filter_params = CostFilter(
        project_id=project_id,
        cost_type=cost_type,
        category=category,
        payment_status=payment_status,
        vendor_id=vendor_id,
        department_id=department_id,
        start_date=start_date,
        end_date=end_date,
        min_amount=min_amount,
        max_amount=max_amount
    )
    return crud.get_costs(db=db, filter_params=filter_params, skip=skip, limit=limit)

@router.put("/{cost_id}", response_model=Cost)
def update_cost(
    *,
    db: Session = Depends(deps.get_db),
    cost_id: int,
    cost_in: CostUpdate,
    current_user: int = Depends(deps.get_current_user)
) -> Cost:
    """
    비용을 업데이트합니다.
    """
    cost = crud.update_cost(db=db, cost_id=cost_id, cost=cost_in, updated_by=current_user)
    if not cost:
        raise HTTPException(status_code=404, detail="비용을 찾을 수 없습니다")
    return cost

@router.delete("/{cost_id}")
def delete_cost(
    *,
    db: Session = Depends(deps.get_db),
    cost_id: int,
    current_user: int = Depends(deps.get_current_user)
) -> dict:
    """
    비용을 삭제합니다.
    """
    if not crud.delete_cost(db=db, cost_id=cost_id):
        raise HTTPException(status_code=404, detail="비용을 찾을 수 없습니다")
    return {"message": "비용이 삭제되었습니다"}

# Cost Attachment 엔드포인트
@router.post("/{cost_id}/attachments", response_model=CostAttachment)
async def create_cost_attachment(
    *,
    db: Session = Depends(deps.get_db),
    cost_id: int,
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    current_user: int = Depends(deps.get_current_user)
) -> CostAttachment:
    """
    비용 첨부파일을 업로드합니다.
    """
    cost = crud.get_cost(db=db, cost_id=cost_id)
    if not cost:
        raise HTTPException(status_code=404, detail="비용을 찾을 수 없습니다")
    
    # 파일 저장
    file_url, file_name, file_size = await file_service.save_file(
        file=file,
        document_type="financial",
        document_id=cost_id
    )
    
    return crud.create_cost_attachment(
        db=db,
        cost_id=cost_id,
        file_name=file_name,
        file_path=file_url,
        file_type=file.content_type,
        file_size=file_size,
        description=description,
        uploaded_by=current_user
    )

@router.get("/{cost_id}/attachments", response_model=List[CostAttachment])
def get_cost_attachments(
    *,
    db: Session = Depends(deps.get_db),
    cost_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: int = Depends(deps.get_current_user)
) -> List[CostAttachment]:
    """
    비용 첨부파일 목록을 조회합니다.
    """
    return crud.get_cost_attachments(db=db, cost_id=cost_id, skip=skip, limit=limit)

@router.delete("/attachments/{attachment_id}")
def delete_cost_attachment(
    *,
    db: Session = Depends(deps.get_db),
    attachment_id: int,
    current_user: int = Depends(deps.get_current_user)
) -> dict:
    """
    비용 첨부파일을 삭제합니다.
    """
    if not crud.delete_cost_attachment(db=db, attachment_id=attachment_id):
        raise HTTPException(status_code=404, detail="첨부파일을 찾을 수 없습니다")
    return {"message": "첨부파일이 삭제되었습니다"}

# Cost Approval 엔드포인트
@router.post("/{cost_id}/approvals", response_model=CostApproval)
def create_cost_approval(
    *,
    db: Session = Depends(deps.get_db),
    cost_id: int,
    status: str = Query(..., description="승인 상태 (approved/rejected)"),
    comment: Optional[str] = None,
    current_user: int = Depends(deps.get_current_user)
) -> CostApproval:
    """
    비용 승인을 생성합니다.
    """
    cost = crud.get_cost(db=db, cost_id=cost_id)
    if not cost:
        raise HTTPException(status_code=404, detail="비용을 찾을 수 없습니다")
    
    return crud.create_cost_approval(
        db=db,
        cost_id=cost_id,
        approver_id=current_user,
        status=status,
        comment=comment
    )

@router.get("/{cost_id}/approvals", response_model=List[CostApproval])
def get_cost_approvals(
    *,
    db: Session = Depends(deps.get_db),
    cost_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: int = Depends(deps.get_current_user)
) -> List[CostApproval]:
    """
    비용 승인 목록을 조회합니다.
    """
    return crud.get_cost_approvals(db=db, cost_id=cost_id, skip=skip, limit=limit)

# Cost Statistics 엔드포인트
@router.get("/statistics", response_model=CostStatistics)
def get_cost_statistics(
    *,
    db: Session = Depends(deps.get_db),
    project_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: int = Depends(deps.get_current_user)
) -> CostStatistics:
    """
    비용 통계를 조회합니다.
    """
    return crud.get_cost_statistics(
        db=db,
        project_id=project_id,
        start_date=start_date,
        end_date=end_date
    ) 