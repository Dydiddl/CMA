from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.api.deps import get_db
from ....schemas.labor import (
    Labor,
    LaborCreate,
    LaborUpdate,
    WorkLog,
    WorkLogCreate,
    WorkLogUpdate
)
from ....services import labor as labor_service

router = APIRouter()

@router.post("/", response_model=Labor, description="새로운 근로자를 등록합니다.")
def create_labor(
    labor: LaborCreate,
    db: Session = Depends(get_db)
):
    """새로운 근로자를 등록합니다."""
    return labor_service.create_labor(db=db, labor=labor)

@router.get("/", response_model=List[Labor], description="근로자 목록을 조회합니다.")
def read_labors(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    contract_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """근로자 목록을 조회합니다."""
    return labor_service.get_labors(
        db=db,
        skip=skip,
        limit=limit,
        status=status,
        contract_id=contract_id
    )

@router.get("/{labor_id}", response_model=Labor, description="특정 근로자의 상세 정보를 조회합니다.")
def read_labor(
    labor_id: int,
    db: Session = Depends(get_db)
):
    """특정 근로자의 상세 정보를 조회합니다."""
    labor = labor_service.get_labor(db=db, labor_id=labor_id)
    if labor is None:
        raise HTTPException(status_code=404, detail="근로자를 찾을 수 없습니다")
    return labor

@router.put("/{labor_id}", response_model=Labor, description="근로자 정보를 업데이트합니다.")
def update_labor(
    labor_id: int,
    labor: LaborUpdate,
    db: Session = Depends(get_db)
):
    """근로자 정보를 업데이트합니다."""
    updated_labor = labor_service.update_labor(
        db=db,
        labor_id=labor_id,
        labor=labor
    )
    if updated_labor is None:
        raise HTTPException(status_code=404, detail="근로자를 찾을 수 없습니다")
    return updated_labor

@router.delete("/{labor_id}", description="근로자를 삭제합니다.")
def delete_labor(
    labor_id: int,
    db: Session = Depends(get_db)
):
    """근로자를 삭제합니다."""
    success = labor_service.delete_labor(db=db, labor_id=labor_id)
    if not success:
        raise HTTPException(status_code=404, detail="근로자를 찾을 수 없습니다")
    return {"message": "근로자가 삭제되었습니다"}

@router.post("/{labor_id}/work-logs", response_model=WorkLog, description="근로자의 작업일지를 등록합니다.")
def create_work_log(
    labor_id: int,
    work_log: WorkLogCreate,
    db: Session = Depends(get_db)
):
    """근로자의 작업일지를 등록합니다."""
    return labor_service.create_work_log(
        db=db,
        labor_id=labor_id,
        work_log=work_log
    )

@router.get("/{labor_id}/work-logs", response_model=List[WorkLog], description="근로자의 작업일지 목록을 조회합니다.")
def read_work_logs(
    labor_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """근로자의 작업일지 목록을 조회합니다."""
    return labor_service.get_work_logs(
        db=db,
        labor_id=labor_id,
        start_date=start_date,
        end_date=end_date,
        status=status
    )

@router.put("/{labor_id}/work-logs/{work_log_id}", response_model=WorkLog, description="작업일지를 업데이트합니다.")
def update_work_log(
    labor_id: int,
    work_log_id: int,
    work_log: WorkLogUpdate,
    db: Session = Depends(get_db)
):
    """작업일지를 업데이트합니다."""
    updated_work_log = labor_service.update_work_log(
        db=db,
        labor_id=labor_id,
        work_log_id=work_log_id,
        work_log=work_log
    )
    if updated_work_log is None:
        raise HTTPException(status_code=404, detail="작업일지를 찾을 수 없습니다")
    return updated_work_log 