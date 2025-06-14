from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta

from app.models.cost import Cost, CostAttachment, CostApproval, CostType, PaymentStatus, CostCategory
from app.schemas.cost import CostCreate, CostUpdate, CostFilter, CostStatistics

def create_cost(db: Session, cost: CostCreate, created_by: int) -> Cost:
    """비용을 생성합니다."""
    db_cost = Cost(
        **cost.dict(),
        created_by=created_by,
        payment_status=PaymentStatus.PENDING
    )
    db.add(db_cost)
    db.commit()
    db.refresh(db_cost)
    return db_cost

def get_cost(db: Session, cost_id: int) -> Optional[Cost]:
    """비용을 조회합니다."""
    return db.query(Cost).filter(Cost.id == cost_id).first()

def get_costs(
    db: Session,
    filter_params: CostFilter,
    skip: int = 0,
    limit: int = 100
) -> List[Cost]:
    """비용 목록을 조회합니다."""
    query = db.query(Cost)
    
    # 필터 적용
    if filter_params.project_id:
        query = query.filter(Cost.project_id == filter_params.project_id)
    if filter_params.cost_type:
        query = query.filter(Cost.cost_type == filter_params.cost_type)
    if filter_params.category:
        query = query.filter(Cost.category == filter_params.category)
    if filter_params.payment_status:
        query = query.filter(Cost.payment_status == filter_params.payment_status)
    if filter_params.vendor_id:
        query = query.filter(Cost.vendor_id == filter_params.vendor_id)
    if filter_params.department_id:
        query = query.filter(Cost.department_id == filter_params.department_id)
    if filter_params.start_date:
        query = query.filter(Cost.payment_date >= filter_params.start_date)
    if filter_params.end_date:
        query = query.filter(Cost.payment_date <= filter_params.end_date)
    if filter_params.min_amount:
        query = query.filter(Cost.amount >= filter_params.min_amount)
    if filter_params.max_amount:
        query = query.filter(Cost.amount <= filter_params.max_amount)
    
    return query.offset(skip).limit(limit).all()

def update_cost(
    db: Session,
    cost_id: int,
    cost: CostUpdate,
    updated_by: int
) -> Optional[Cost]:
    """비용을 업데이트합니다."""
    db_cost = get_cost(db, cost_id)
    if not db_cost:
        return None
    
    update_data = cost.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_cost, field, value)
    
    db_cost.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_cost)
    return db_cost

def delete_cost(db: Session, cost_id: int) -> bool:
    """비용을 삭제합니다."""
    db_cost = get_cost(db, cost_id)
    if not db_cost:
        return False
    
    db.delete(db_cost)
    db.commit()
    return True

def create_cost_attachment(
    db: Session,
    cost_id: int,
    file_name: str,
    file_path: str,
    file_type: Optional[str],
    file_size: Optional[int],
    description: Optional[str],
    uploaded_by: int
) -> CostAttachment:
    """비용 첨부파일을 생성합니다."""
    db_attachment = CostAttachment(
        cost_id=cost_id,
        file_name=file_name,
        file_path=file_path,
        file_type=file_type,
        file_size=file_size,
        description=description,
        uploaded_by=uploaded_by
    )
    db.add(db_attachment)
    db.commit()
    db.refresh(db_attachment)
    return db_attachment

def get_cost_attachments(
    db: Session,
    cost_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[CostAttachment]:
    """비용 첨부파일 목록을 조회합니다."""
    return db.query(CostAttachment)\
        .filter(CostAttachment.cost_id == cost_id)\
        .offset(skip)\
        .limit(limit)\
        .all()

def delete_cost_attachment(db: Session, attachment_id: int) -> bool:
    """비용 첨부파일을 삭제합니다."""
    db_attachment = db.query(CostAttachment)\
        .filter(CostAttachment.id == attachment_id)\
        .first()
    if not db_attachment:
        return False
    
    db.delete(db_attachment)
    db.commit()
    return True

def create_cost_approval(
    db: Session,
    cost_id: int,
    approver_id: int,
    status: PaymentStatus,
    comment: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> CostApproval:
    """비용 승인을 생성합니다."""
    db_approval = CostApproval(
        cost_id=cost_id,
        approver_id=approver_id,
        status=status,
        comment=comment,
        metadata=metadata
    )
    db.add(db_approval)
    
    # 비용 상태 업데이트
    db_cost = get_cost(db, cost_id)
    if db_cost:
        db_cost.payment_status = status
        db_cost.approved_by = approver_id
    
    db.commit()
    db.refresh(db_approval)
    return db_approval

def get_cost_approvals(
    db: Session,
    cost_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[CostApproval]:
    """비용 승인 목록을 조회합니다."""
    return db.query(CostApproval)\
        .filter(CostApproval.cost_id == cost_id)\
        .offset(skip)\
        .limit(limit)\
        .all()

def get_cost_statistics(
    db: Session,
    project_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> CostStatistics:
    """비용 통계를 조회합니다."""
    query = db.query(Cost)
    
    if project_id:
        query = query.filter(Cost.project_id == project_id)
    if start_date:
        query = query.filter(Cost.payment_date >= start_date)
    if end_date:
        query = query.filter(Cost.payment_date <= end_date)
    
    # 전체 금액 및 건수
    total_amount = query.with_entities(func.sum(Cost.amount)).scalar() or 0
    count = query.count()
    
    # 유형별 금액
    by_type = {}
    for cost_type in CostType:
        amount = query.filter(Cost.cost_type == cost_type)\
            .with_entities(func.sum(Cost.amount))\
            .scalar() or 0
        by_type[cost_type] = amount
    
    # 카테고리별 금액
    by_category = {}
    for category in CostCategory:
        amount = query.filter(Cost.category == category)\
            .with_entities(func.sum(Cost.amount))\
            .scalar() or 0
        by_category[category] = amount
    
    # 상태별 건수
    by_status = {}
    for status in PaymentStatus:
        count = query.filter(Cost.payment_status == status).count()
        by_status[status] = count
    
    # 부서별 금액
    by_department = {}
    department_amounts = query.with_entities(
        Cost.department_id,
        func.sum(Cost.amount)
    ).group_by(Cost.department_id).all()
    for dept_id, amount in department_amounts:
        by_department[dept_id] = amount
    
    # 거래처별 금액
    by_vendor = {}
    vendor_amounts = query.with_entities(
        Cost.vendor_id,
        func.sum(Cost.amount)
    ).group_by(Cost.vendor_id).all()
    for vendor_id, amount in vendor_amounts:
        by_vendor[vendor_id] = amount
    
    # 월별 금액
    by_month = {}
    month_amounts = query.with_entities(
        func.date_trunc('month', Cost.payment_date),
        func.sum(Cost.amount)
    ).group_by(func.date_trunc('month', Cost.payment_date)).all()
    for month, amount in month_amounts:
        by_month[month.strftime('%Y-%m')] = amount
    
    return CostStatistics(
        total_amount=total_amount,
        count=count,
        by_type=by_type,
        by_category=by_category,
        by_status=by_status,
        by_department=by_department,
        by_vendor=by_vendor,
        by_month=by_month
    ) 