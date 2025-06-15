from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from app.api import deps
from app.core.permissions import check_permissions
from app.models.user import User
from app.schemas.budget import (
    Budget, BudgetCreate, BudgetUpdate,
    BudgetItem, BudgetItemCreate, BudgetItemUpdate,
    BudgetAttachment, BudgetAttachmentCreate,
    BudgetApproval, BudgetApprovalCreate,
    BudgetAlert, BudgetAlertCreate, BudgetAlertUpdate,
    BudgetStatistics
)
from app.crud import budget as budget_crud

router = APIRouter()

# 예산 CRUD
@router.post("/", response_model=Budget)
def create_budget(
    *,
    db: Session = Depends(deps.get_db),
    budget_in: BudgetCreate,
    current_user: User = Depends(deps.get_current_user)
) -> Budget:
    """
    새로운 예산을 생성합니다.
    """
    if not check_permissions(current_user, ["create:budget"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="예산 생성 권한이 없습니다"
        )
    
    budget = budget_crud.create_budget(db=db, budget=budget_in, user_id=current_user.id)
    return budget

@router.get("/{budget_id}", response_model=Budget)
def read_budget(
    *,
    db: Session = Depends(deps.get_db),
    budget_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> Budget:
    """
    ID로 예산을 조회합니다.
    """
    if not check_permissions(current_user, ["read:budget"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="예산 조회 권한이 없습니다"
        )
    
    budget = budget_crud.get_budget(db=db, budget_id=budget_id)
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="예산을 찾을 수 없습니다"
        )
    return budget

@router.get("/", response_model=List[Budget])
def read_budgets(
    *,
    db: Session = Depends(deps.get_db),
    project_id: Optional[int] = None,
    budget_type: Optional[str] = None,
    budget_status: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    created_by: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> List[Budget]:
    """
    예산 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:budget"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="예산 조회 권한이 없습니다"
        )
    
    budgets = budget_crud.get_budgets(
        db=db,
        project_id=project_id,
        budget_type=budget_type,
        budget_status=budget_status,
        start_date=start_date,
        end_date=end_date,
        created_by=created_by,
        skip=skip,
        limit=limit
    )
    return budgets

@router.put("/{budget_id}", response_model=Budget)
def update_budget(
    *,
    db: Session = Depends(deps.get_db),
    budget_id: int,
    budget_in: BudgetUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> Budget:
    """
    예산을 업데이트합니다.
    """
    if not check_permissions(current_user, ["update:budget"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="예산 수정 권한이 없습니다"
        )
    
    budget = budget_crud.get_budget(db=db, budget_id=budget_id)
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="예산을 찾을 수 없습니다"
        )
    
    budget = budget_crud.update_budget(db=db, budget_id=budget_id, budget=budget_in)
    return budget

@router.delete("/{budget_id}")
def delete_budget(
    *,
    db: Session = Depends(deps.get_db),
    budget_id: int,
    current_user: User = Depends(deps.get_current_user)
):
    """
    예산을 삭제합니다.
    """
    if not check_permissions(current_user, ["delete:budget"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="예산 삭제 권한이 없습니다"
        )
    
    budget = budget_crud.get_budget(db=db, budget_id=budget_id)
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="예산을 찾을 수 없습니다"
        )
    
    budget_crud.delete_budget(db=db, budget_id=budget_id)
    return {"status": "success"}

# 예산 항목 CRUD
@router.post("/{budget_id}/items", response_model=BudgetItem)
def create_budget_item(
    *,
    db: Session = Depends(deps.get_db),
    budget_id: int,
    item_in: BudgetItemCreate,
    current_user: User = Depends(deps.get_current_user)
) -> BudgetItem:
    """
    예산 항목을 생성합니다.
    """
    if not check_permissions(current_user, ["create:budget_item"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="예산 항목 생성 권한이 없습니다"
        )
    
    budget = budget_crud.get_budget(db=db, budget_id=budget_id)
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="예산을 찾을 수 없습니다"
        )
    
    item = budget_crud.create_budget_item(db=db, budget_id=budget_id, item=item_in)
    return item

@router.get("/{budget_id}/items", response_model=List[BudgetItem])
def read_budget_items(
    *,
    db: Session = Depends(deps.get_db),
    budget_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> List[BudgetItem]:
    """
    예산 항목 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:budget_item"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="예산 항목 조회 권한이 없습니다"
        )
    
    items = budget_crud.get_budget_items(db=db, budget_id=budget_id, skip=skip, limit=limit)
    return items

@router.put("/items/{item_id}", response_model=BudgetItem)
def update_budget_item(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
    item_in: BudgetItemUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> BudgetItem:
    """
    예산 항목을 업데이트합니다.
    """
    if not check_permissions(current_user, ["update:budget_item"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="예산 항목 수정 권한이 없습니다"
        )
    
    item = budget_crud.get_budget_item(db=db, item_id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="예산 항목을 찾을 수 없습니다"
        )
    
    item = budget_crud.update_budget_item(db=db, item_id=item_id, item=item_in)
    return item

@router.delete("/items/{item_id}")
def delete_budget_item(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
    current_user: User = Depends(deps.get_current_user)
):
    """
    예산 항목을 삭제합니다.
    """
    if not check_permissions(current_user, ["delete:budget_item"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="예산 항목 삭제 권한이 없습니다"
        )
    
    item = budget_crud.get_budget_item(db=db, item_id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="예산 항목을 찾을 수 없습니다"
        )
    
    budget_crud.delete_budget_item(db=db, item_id=item_id)
    return {"status": "success"}

# 첨부파일 CRUD
@router.post("/{budget_id}/attachments", response_model=BudgetAttachment)
async def create_budget_attachment(
    *,
    db: Session = Depends(deps.get_db),
    budget_id: int,
    file: UploadFile = File(...),
    description: Optional[str] = None,
    current_user: User = Depends(deps.get_current_user)
) -> BudgetAttachment:
    """
    예산 첨부파일을 업로드합니다.
    """
    if not check_permissions(current_user, ["create:budget_attachment"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="예산 첨부파일 업로드 권한이 없습니다"
        )
    
    budget = budget_crud.get_budget(db=db, budget_id=budget_id)
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="예산을 찾을 수 없습니다"
        )
    
    # 파일 저장 로직 구현 필요
    file_path = f"uploads/budgets/{budget_id}/{file.filename}"
    
    attachment_in = BudgetAttachmentCreate(
        file_name=file.filename,
        file_path=file_path,
        file_type=file.content_type,
        file_size=file.size,
        description=description
    )
    
    attachment = budget_crud.create_budget_attachment(
        db=db,
        budget_id=budget_id,
        attachment=attachment_in
    )
    return attachment

@router.get("/{budget_id}/attachments", response_model=List[BudgetAttachment])
def read_budget_attachments(
    *,
    db: Session = Depends(deps.get_db),
    budget_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> List[BudgetAttachment]:
    """
    예산 첨부파일 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:budget_attachment"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="예산 첨부파일 조회 권한이 없습니다"
        )
    
    attachments = budget_crud.get_budget_attachments(
        db=db,
        budget_id=budget_id,
        skip=skip,
        limit=limit
    )
    return attachments

@router.delete("/attachments/{attachment_id}")
def delete_budget_attachment(
    *,
    db: Session = Depends(deps.get_db),
    attachment_id: int,
    current_user: User = Depends(deps.get_current_user)
):
    """
    예산 첨부파일을 삭제합니다.
    """
    if not check_permissions(current_user, ["delete:budget_attachment"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="예산 첨부파일 삭제 권한이 없습니다"
        )
    
    attachment = budget_crud.get_budget_attachment(db=db, attachment_id=attachment_id)
    if not attachment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="예산 첨부파일을 찾을 수 없습니다"
        )
    
    budget_crud.delete_budget_attachment(db=db, attachment_id=attachment_id)
    return {"status": "success"}

# 예산 승인 관리
@router.post("/{budget_id}/approvals", response_model=BudgetApproval)
def create_budget_approval(
    *,
    db: Session = Depends(deps.get_db),
    budget_id: int,
    approval_in: BudgetApprovalCreate,
    current_user: User = Depends(deps.get_current_user)
) -> BudgetApproval:
    """
    예산 승인을 생성합니다.
    """
    if not check_permissions(current_user, ["create:budget_approval"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="예산 승인 생성 권한이 없습니다"
        )
    
    budget = budget_crud.get_budget(db=db, budget_id=budget_id)
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="예산을 찾을 수 없습니다"
        )
    
    approval = budget_crud.create_budget_approval(
        db=db,
        budget_id=budget_id,
        approval=approval_in,
        user_id=current_user.id
    )
    return approval

@router.get("/{budget_id}/approvals", response_model=List[BudgetApproval])
def read_budget_approvals(
    *,
    db: Session = Depends(deps.get_db),
    budget_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> List[BudgetApproval]:
    """
    예산 승인 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:budget_approval"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="예산 승인 조회 권한이 없습니다"
        )
    
    approvals = budget_crud.get_budget_approvals(
        db=db,
        budget_id=budget_id,
        skip=skip,
        limit=limit
    )
    return approvals

# 예산 알림 관리
@router.post("/{budget_id}/alerts", response_model=BudgetAlert)
def create_budget_alert(
    *,
    db: Session = Depends(deps.get_db),
    budget_id: int,
    alert_in: BudgetAlertCreate,
    current_user: User = Depends(deps.get_current_user)
) -> BudgetAlert:
    """
    예산 알림을 생성합니다.
    """
    if not check_permissions(current_user, ["create:budget_alert"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="예산 알림 생성 권한이 없습니다"
        )
    
    budget = budget_crud.get_budget(db=db, budget_id=budget_id)
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="예산을 찾을 수 없습니다"
        )
    
    alert = budget_crud.create_budget_alert(
        db=db,
        budget_id=budget_id,
        alert=alert_in,
        user_id=current_user.id
    )
    return alert

@router.get("/{budget_id}/alerts", response_model=List[BudgetAlert])
def read_budget_alerts(
    *,
    db: Session = Depends(deps.get_db),
    budget_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> List[BudgetAlert]:
    """
    예산 알림 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:budget_alert"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="예산 알림 조회 권한이 없습니다"
        )
    
    alerts = budget_crud.get_budget_alerts(
        db=db,
        budget_id=budget_id,
        skip=skip,
        limit=limit
    )
    return alerts

@router.put("/alerts/{alert_id}", response_model=BudgetAlert)
def update_budget_alert(
    *,
    db: Session = Depends(deps.get_db),
    alert_id: int,
    alert_in: BudgetAlertUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> BudgetAlert:
    """
    예산 알림을 업데이트합니다.
    """
    if not check_permissions(current_user, ["update:budget_alert"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="예산 알림 수정 권한이 없습니다"
        )
    
    alert = budget_crud.get_budget_alert(db=db, alert_id=alert_id)
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="예산 알림을 찾을 수 없습니다"
        )
    
    alert = budget_crud.update_budget_alert(db=db, alert_id=alert_id, alert=alert_in)
    return alert

@router.delete("/alerts/{alert_id}")
def delete_budget_alert(
    *,
    db: Session = Depends(deps.get_db),
    alert_id: int,
    current_user: User = Depends(deps.get_current_user)
):
    """
    예산 알림을 삭제합니다.
    """
    if not check_permissions(current_user, ["delete:budget_alert"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="예산 알림 삭제 권한이 없습니다"
        )
    
    alert = budget_crud.get_budget_alert(db=db, alert_id=alert_id)
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="예산 알림을 찾을 수 없습니다"
        )
    
    budget_crud.delete_budget_alert(db=db, alert_id=alert_id)
    return {"status": "success"}

# 예산 통계
@router.get("/statistics/{project_id}", response_model=BudgetStatistics)
def read_budget_statistics(
    *,
    db: Session = Depends(deps.get_db),
    project_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> BudgetStatistics:
    """
    프로젝트의 예산 통계를 조회합니다.
    """
    if not check_permissions(current_user, ["read:budget_statistics"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="예산 통계 조회 권한이 없습니다"
        )
    
    statistics = budget_crud.get_budget_statistics(db=db, project_id=project_id)
    return statistics 