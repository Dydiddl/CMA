from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from ..models.labor import Labor, WorkLog
from ..schemas.labor import (
    LaborCreate,
    LaborUpdate,
    WorkLogCreate
)

def create_labor(db: Session, labor: LaborCreate) -> Labor:
    """새로운 노무자를 등록합니다."""
    db_labor = Labor(**labor.dict())
    db.add(db_labor)
    db.commit()
    db.refresh(db_labor)
    return db_labor

def get_labors(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    contract_id: Optional[str] = None
) -> List[Labor]:
    """노무자 목록을 조회합니다."""
    query = db.query(Labor)
    if status:
        query = query.filter(Labor.status == status)
    if contract_id:
        query = query.filter(Labor.contract_id == contract_id)
    return query.offset(skip).limit(limit).all()

def get_labor(db: Session, labor_id: int) -> Optional[Labor]:
    """특정 노무자의 정보를 조회합니다."""
    return db.query(Labor).filter(Labor.id == labor_id).first()

def update_labor(
    db: Session,
    labor_id: int,
    labor: LaborUpdate
) -> Optional[Labor]:
    """노무자 정보를 업데이트합니다."""
    db_labor = get_labor(db, labor_id)
    if db_labor:
        for key, value in labor.dict(exclude_unset=True).items():
            setattr(db_labor, key, value)
        db.commit()
        db.refresh(db_labor)
    return db_labor

def delete_labor(db: Session, labor_id: int) -> bool:
    """노무자를 삭제합니다."""
    db_labor = get_labor(db, labor_id)
    if db_labor:
        db.delete(db_labor)
        db.commit()
        return True
    return False

def create_work_log(
    db: Session,
    labor_id: int,
    log: WorkLogCreate
) -> WorkLog:
    """근무 기록을 생성합니다."""
    db_log = WorkLog(**log.dict(), labor_id=labor_id)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_work_logs(
    db: Session,
    labor_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> List[WorkLog]:
    """노무자의 근무 기록을 조회합니다."""
    query = db.query(WorkLog).filter(WorkLog.labor_id == labor_id)
    if start_date:
        query = query.filter(WorkLog.work_date >= start_date)
    if end_date:
        query = query.filter(WorkLog.work_date <= end_date)
    return query.all() 