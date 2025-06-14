from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.core.permissions import check_permissions
from app.models.user import User
from app.schemas.notification import (
    NotificationCreate, NotificationUpdate, Notification,
    NotificationTemplate, NotificationTemplateCreate,
    NotificationStats
)
from app.crud import notification as notification_crud

router = APIRouter()

# 알림 기본 CRUD
@router.post("/", response_model=Notification)
def create_notification(
    *,
    db: Session = Depends(deps.get_db),
    notification_in: NotificationCreate,
    current_user: User = Depends(deps.get_current_user)
) -> Notification:
    """
    새로운 알림을 생성합니다.
    """
    if not check_permissions(current_user, ["create:notification"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="알림 생성 권한이 없습니다"
        )
    
    notification = notification_crud.create(
        db=db,
        obj_in=notification_in,
        creator_id=current_user.id
    )
    return notification

@router.get("/", response_model=List[Notification])
def read_notifications(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    is_read: Optional[bool] = None,
    notification_type: Optional[str] = None,
    current_user: User = Depends(deps.get_current_user)
) -> List[Notification]:
    """
    알림 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:notification"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="알림 조회 권한이 없습니다"
        )
    
    notifications = notification_crud.get_multi(
        db=db,
        skip=skip,
        limit=limit,
        user_id=current_user.id,
        is_read=is_read,
        notification_type=notification_type
    )
    return notifications

@router.get("/{notification_id}", response_model=Notification)
def read_notification(
    *,
    db: Session = Depends(deps.get_db),
    notification_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> Notification:
    """
    특정 알림을 조회합니다.
    """
    if not check_permissions(current_user, ["read:notification"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="알림 조회 권한이 없습니다"
        )
    
    notification = notification_crud.get(db=db, id=notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="알림을 찾을 수 없습니다"
        )
    
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="다른 사용자의 알림을 조회할 수 없습니다"
        )
    
    return notification

@router.put("/{notification_id}", response_model=Notification)
def update_notification(
    *,
    db: Session = Depends(deps.get_db),
    notification_id: int,
    notification_in: NotificationUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> Notification:
    """
    알림 정보를 업데이트합니다.
    """
    if not check_permissions(current_user, ["update:notification"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="알림 수정 권한이 없습니다"
        )
    
    notification = notification_crud.get(db=db, id=notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="알림을 찾을 수 없습니다"
        )
    
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="다른 사용자의 알림을 수정할 수 없습니다"
        )
    
    notification = notification_crud.update(
        db=db,
        db_obj=notification,
        obj_in=notification_in
    )
    return notification

@router.delete("/{notification_id}")
def delete_notification(
    *,
    db: Session = Depends(deps.get_db),
    notification_id: int,
    current_user: User = Depends(deps.get_current_user)
):
    """
    알림을 삭제합니다.
    """
    if not check_permissions(current_user, ["delete:notification"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="알림 삭제 권한이 없습니다"
        )
    
    notification = notification_crud.get(db=db, id=notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="알림을 찾을 수 없습니다"
        )
    
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="다른 사용자의 알림을 삭제할 수 없습니다"
        )
    
    notification_crud.remove(db=db, id=notification_id)
    return {"status": "success"}

# 알림 템플릿 관리
@router.post("/templates", response_model=NotificationTemplate)
def create_template(
    *,
    db: Session = Depends(deps.get_db),
    template_in: NotificationTemplateCreate,
    current_user: User = Depends(deps.get_current_user)
) -> NotificationTemplate:
    """
    새로운 알림 템플릿을 생성합니다.
    """
    if not check_permissions(current_user, ["manage:notification_templates"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="알림 템플릿 생성 권한이 없습니다"
        )
    
    template = notification_crud.create_template(
        db=db,
        template_in=template_in,
        creator_id=current_user.id
    )
    return template

# 알림 통계
@router.get("/stats", response_model=NotificationStats)
def get_notification_stats(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> NotificationStats:
    """
    알림 통계를 조회합니다.
    """
    if not check_permissions(current_user, ["read:notification_stats"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="알림 통계 조회 권한이 없습니다"
        )
    
    stats = notification_crud.get_stats(db=db, user_id=current_user.id)
    return stats 