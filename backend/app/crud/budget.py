from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_

from backend.app.models.budget import Budget, BudgetItem, BudgetAttachment, BudgetApproval, BudgetAlert, BudgetStatus
from backend.app.schemas.budget import BudgetCreate, BudgetUpdate, BudgetItemCreate, BudgetItemUpdate, BudgetAttachmentCreate, BudgetApprovalCreate, BudgetAlertCreate, BudgetAlertUpdate

def create_budget(db: Session, budget: BudgetCreate, user_id: int) -> Budget:
    db_budget = Budget(
        **budget.dict(),
        budget_status=BudgetStatus.DRAFT,
        version=1,
        created_by=user_id
    )
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

def get_budget(db: Session, budget_id: int) -> Optional[Budget]:
    return db.query(Budget).filter(Budget.id == budget_id).first()

def get_budgets(
    db: Session,
    project_id: Optional[int] = None,
    budget_type: Optional[str] = None,
    budget_status: Optional[BudgetStatus] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    created_by: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Budget]:
    query = db.query(Budget)
    
    if project_id:
        query = query.filter(Budget.project_id == project_id)
    if budget_type:
        query = query.filter(Budget.budget_type == budget_type)
    if budget_status:
        query = query.filter(Budget.budget_status == budget_status)
    if start_date:
        query = query.filter(Budget.start_date >= start_date)
    if end_date:
        query = query.filter(Budget.end_date <= end_date)
    if created_by:
        query = query.filter(Budget.created_by == created_by)
        
    return query.offset(skip).limit(limit).all()

def update_budget(db: Session, budget_id: int, budget: BudgetUpdate) -> Optional[Budget]:
    db_budget = get_budget(db, budget_id)
    if not db_budget:
        return None
        
    update_data = budget.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_budget, field, value)
    
    db_budget.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_budget)
    return db_budget

def delete_budget(db: Session, budget_id: int) -> bool:
    db_budget = get_budget(db, budget_id)
    if not db_budget:
        return False
        
    db.delete(db_budget)
    db.commit()
    return True

# 예산 항목 CRUD
def create_budget_item(db: Session, budget_id: int, item: BudgetItemCreate) -> BudgetItem:
    db_item = BudgetItem(**item.dict(), budget_id=budget_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_budget_item(db: Session, item_id: int) -> Optional[BudgetItem]:
    return db.query(BudgetItem).filter(BudgetItem.id == item_id).first()

def get_budget_items(db: Session, budget_id: int, skip: int = 0, limit: int = 100) -> List[BudgetItem]:
    return db.query(BudgetItem).filter(BudgetItem.budget_id == budget_id).offset(skip).limit(limit).all()

def update_budget_item(db: Session, item_id: int, item: BudgetItemUpdate) -> Optional[BudgetItem]:
    db_item = get_budget_item(db, item_id)
    if not db_item:
        return None
        
    update_data = item.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db_item.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_budget_item(db: Session, item_id: int) -> bool:
    db_item = get_budget_item(db, item_id)
    if not db_item:
        return False
        
    db.delete(db_item)
    db.commit()
    return True

# 첨부파일 CRUD
def create_budget_attachment(db: Session, budget_id: int, attachment: BudgetAttachmentCreate, user_id: int) -> BudgetAttachment:
    db_attachment = BudgetAttachment(**attachment.dict(), budget_id=budget_id, uploaded_by=user_id)
    db.add(db_attachment)
    db.commit()
    db.refresh(db_attachment)
    return db_attachment

def get_budget_attachment(db: Session, attachment_id: int) -> Optional[BudgetAttachment]:
    return db.query(BudgetAttachment).filter(BudgetAttachment.id == attachment_id).first()

def get_budget_attachments(db: Session, budget_id: int, skip: int = 0, limit: int = 100) -> List[BudgetAttachment]:
    return db.query(BudgetAttachment).filter(BudgetAttachment.budget_id == budget_id).offset(skip).limit(limit).all()

def delete_budget_attachment(db: Session, attachment_id: int) -> bool:
    db_attachment = get_budget_attachment(db, attachment_id)
    if not db_attachment:
        return False
        
    db.delete(db_attachment)
    db.commit()
    return True

# 승인 CRUD
def create_budget_approval(db: Session, budget_id: int, approval: BudgetApprovalCreate, approver_id: int) -> BudgetApproval:
    db_approval = BudgetApproval(**approval.dict(), budget_id=budget_id, approver_id=approver_id)
    db.add(db_approval)
    
    # 예산 상태 업데이트
    db_budget = get_budget(db, budget_id)
    if db_budget:
        db_budget.budget_status = approval.status
        db_budget.approved_by = approver_id
        db_budget.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_approval)
    return db_approval

def get_budget_approvals(db: Session, budget_id: int, skip: int = 0, limit: int = 100) -> List[BudgetApproval]:
    return db.query(BudgetApproval).filter(BudgetApproval.budget_id == budget_id).offset(skip).limit(limit).all()

# 알림 CRUD
def create_budget_alert(db: Session, budget_id: int, alert: BudgetAlertCreate) -> BudgetAlert:
    db_alert = BudgetAlert(**alert.dict(), budget_id=budget_id)
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

def get_budget_alert(db: Session, alert_id: int) -> Optional[BudgetAlert]:
    return db.query(BudgetAlert).filter(BudgetAlert.id == alert_id).first()

def get_budget_alerts(db: Session, budget_id: int, skip: int = 0, limit: int = 100) -> List[BudgetAlert]:
    return db.query(BudgetAlert).filter(BudgetAlert.budget_id == budget_id).offset(skip).limit(limit).all()

def update_budget_alert(db: Session, alert_id: int, alert: BudgetAlertUpdate) -> Optional[BudgetAlert]:
    db_alert = get_budget_alert(db, alert_id)
    if not db_alert:
        return None
        
    update_data = alert.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_alert, field, value)
    
    db_alert.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_alert)
    return db_alert

def delete_budget_alert(db: Session, alert_id: int) -> bool:
    db_alert = get_budget_alert(db, alert_id)
    if not db_alert:
        return False
        
    db.delete(db_alert)
    db.commit()
    return True

# 통계 조회
def get_budget_statistics(db: Session, project_id: int) -> Dict[str, Any]:
    # 기본 통계
    total_budgets = db.query(func.count(Budget.id)).filter(Budget.project_id == project_id).scalar()
    total_amount = db.query(func.sum(Budget.total_amount)).filter(Budget.project_id == project_id).scalar() or 0
    
    # 상태별 분포
    status_distribution = dict(
        db.query(Budget.budget_status, func.count(Budget.id))
        .filter(Budget.project_id == project_id)
        .group_by(Budget.budget_status)
        .all()
    )
    
    # 카테고리별 분포
    category_distribution = dict(
        db.query(BudgetItem.category, func.sum(BudgetItem.amount))
        .join(Budget)
        .filter(Budget.project_id == project_id)
        .group_by(BudgetItem.category)
        .all()
    )
    
    # 월별 추이
    monthly_trend = dict(
        db.query(
            func.date_trunc('month', Budget.created_at).label('month'),
            func.sum(Budget.total_amount)
        )
        .filter(Budget.project_id == project_id)
        .group_by('month')
        .all()
    )
    
    # 알림 수
    alert_count = db.query(func.count(BudgetAlert.id))\
        .join(Budget)\
        .filter(Budget.project_id == project_id)\
        .scalar()
    
    return {
        "total_budgets": total_budgets,
        "total_amount": total_amount,
        "budget_status_distribution": status_distribution,
        "category_distribution": category_distribution,
        "monthly_trend": monthly_trend,
        "alert_count": alert_count
    } 