from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.api import deps
from app.core.permissions import check_permissions
from app.models.user import User
from app.schemas.labor import (
    WorkerCreate, WorkerUpdate, Worker,
    SafetyTrainingCreate, SafetyTrainingUpdate, SafetyTraining,
    CertificationCreate, CertificationUpdate, Certification,
    AttendanceRecordCreate, AttendanceRecordUpdate, AttendanceRecord,
    PayrollRecordCreate, PayrollRecordUpdate, PayrollRecord,
    WorkerFilter, SafetyTrainingFilter, CertificationFilter,
    AttendanceFilter, PayrollFilter
)
from app.crud import labor as labor_crud

router = APIRouter()

# 작업자 관리
@router.post("/workers", response_model=Worker)
def create_worker(
    *,
    db: Session = Depends(deps.get_db),
    worker_in: WorkerCreate,
    current_user: User = Depends(deps.get_current_user)
) -> Worker:
    """
    새로운 작업자를 등록합니다.
    """
    if not check_permissions(current_user, ["create:worker"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="작업자 등록 권한이 없습니다"
        )
    
    worker = labor_crud.create_worker(db=db, worker=worker_in)
    return worker

@router.get("/workers", response_model=List[Worker])
def read_workers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    worker_type: Optional[str] = None,
    status: Optional[str] = None,
    hire_date_from: Optional[datetime] = None,
    hire_date_to: Optional[datetime] = None,
    current_user: User = Depends(deps.get_current_user)
) -> List[Worker]:
    """
    작업자 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:worker"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="작업자 조회 권한이 없습니다"
        )
    
    filters = WorkerFilter(
        name=name,
        worker_type=worker_type,
        status=status,
        hire_date_from=hire_date_from,
        hire_date_to=hire_date_to
    )
    workers = labor_crud.get_workers(
        db=db,
        skip=skip,
        limit=limit,
        filters=filters.dict(exclude_none=True)
    )
    return workers

@router.get("/workers/{worker_id}", response_model=Worker)
def read_worker(
    *,
    db: Session = Depends(deps.get_db),
    worker_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> Worker:
    """
    특정 작업자의 정보를 조회합니다.
    """
    if not check_permissions(current_user, ["read:worker"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="작업자 조회 권한이 없습니다"
        )
    
    worker = labor_crud.get_worker(db=db, worker_id=worker_id)
    if not worker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="작업자를 찾을 수 없습니다"
        )
    return worker

@router.put("/workers/{worker_id}", response_model=Worker)
def update_worker(
    *,
    db: Session = Depends(deps.get_db),
    worker_id: int,
    worker_in: WorkerUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> Worker:
    """
    작업자 정보를 업데이트합니다.
    """
    if not check_permissions(current_user, ["update:worker"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="작업자 정보 수정 권한이 없습니다"
        )
    
    worker = labor_crud.get_worker(db=db, worker_id=worker_id)
    if not worker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="작업자를 찾을 수 없습니다"
        )
    
    worker = labor_crud.update_worker(
        db=db,
        worker_id=worker_id,
        worker=worker_in
    )
    return worker

@router.delete("/workers/{worker_id}")
def delete_worker(
    *,
    db: Session = Depends(deps.get_db),
    worker_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> dict:
    """
    작업자 정보를 삭제합니다.
    """
    if not check_permissions(current_user, ["delete:worker"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="작업자 삭제 권한이 없습니다"
        )
    
    worker = labor_crud.get_worker(db=db, worker_id=worker_id)
    if not worker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="작업자를 찾을 수 없습니다"
        )
    
    labor_crud.delete_worker(db=db, worker_id=worker_id)
    return {"message": "작업자 정보가 삭제되었습니다"}

# 근태 관리
@router.post("/attendance", response_model=AttendanceRecord)
def create_attendance_record(
    *,
    db: Session = Depends(deps.get_db),
    attendance_in: AttendanceRecordCreate,
    current_user: User = Depends(deps.get_current_user)
) -> AttendanceRecord:
    """
    새로운 근태 기록을 생성합니다.
    """
    if not check_permissions(current_user, ["create:attendance"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="근태 기록 생성 권한이 없습니다"
        )
    
    attendance = labor_crud.create_attendance_record(
        db=db,
        attendance=attendance_in,
        creator_id=current_user.id
    )
    return attendance

@router.get("/attendance", response_model=List[AttendanceRecord])
def read_attendance_records(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    worker_id: Optional[int] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    status: Optional[str] = None,
    current_user: User = Depends(deps.get_current_user)
) -> List[AttendanceRecord]:
    """
    근태 기록 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:attendance"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="근태 기록 조회 권한이 없습니다"
        )
    
    filters = AttendanceFilter(
        worker_id=worker_id,
        date_from=date_from,
        date_to=date_to,
        status=status
    )
    attendance_records = labor_crud.get_attendance_records(
        db=db,
        skip=skip,
        limit=limit,
        filters=filters.dict(exclude_none=True)
    )
    return attendance_records

@router.get("/attendance/{attendance_id}", response_model=AttendanceRecord)
def read_attendance_record(
    *,
    db: Session = Depends(deps.get_db),
    attendance_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> AttendanceRecord:
    """
    특정 근태 기록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:attendance"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="근태 기록 조회 권한이 없습니다"
        )
    
    attendance = labor_crud.get_attendance_record(db=db, attendance_id=attendance_id)
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="근태 기록을 찾을 수 없습니다"
        )
    return attendance

@router.put("/attendance/{attendance_id}", response_model=AttendanceRecord)
def update_attendance_record(
    *,
    db: Session = Depends(deps.get_db),
    attendance_id: int,
    attendance_in: AttendanceRecordUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> AttendanceRecord:
    """
    근태 기록을 업데이트합니다.
    """
    if not check_permissions(current_user, ["update:attendance"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="근태 기록 수정 권한이 없습니다"
        )
    
    attendance = labor_crud.get_attendance_record(db=db, attendance_id=attendance_id)
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="근태 기록을 찾을 수 없습니다"
        )
    
    attendance = labor_crud.update_attendance_record(
        db=db,
        attendance_id=attendance_id,
        attendance=attendance_in
    )
    return attendance

@router.delete("/attendance/{attendance_id}")
def delete_attendance_record(
    *,
    db: Session = Depends(deps.get_db),
    attendance_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> dict:
    """
    근태 기록을 삭제합니다.
    """
    if not check_permissions(current_user, ["delete:attendance"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="근태 기록 삭제 권한이 없습니다"
        )
    
    attendance = labor_crud.get_attendance_record(db=db, attendance_id=attendance_id)
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="근태 기록을 찾을 수 없습니다"
        )
    
    labor_crud.delete_attendance_record(db=db, attendance_id=attendance_id)
    return {"message": "근태 기록이 삭제되었습니다"}

# 안전 교육 관리
@router.post("/safety-trainings", response_model=SafetyTraining)
def create_safety_training(
    *,
    db: Session = Depends(deps.get_db),
    training_in: SafetyTrainingCreate,
    current_user: User = Depends(deps.get_current_user)
) -> SafetyTraining:
    """
    새로운 안전 교육 기록을 생성합니다.
    """
    if not check_permissions(current_user, ["create:safety_training"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="안전 교육 기록 생성 권한이 없습니다"
        )
    
    training = labor_crud.create_safety_training(
        db=db,
        training=training_in,
        creator_id=current_user.id
    )
    return training

@router.get("/safety-trainings", response_model=List[SafetyTraining])
def read_safety_trainings(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    worker_id: Optional[int] = None,
    training_date_from: Optional[datetime] = None,
    training_date_to: Optional[datetime] = None,
    training_type: Optional[str] = None,
    passed: Optional[bool] = None,
    current_user: User = Depends(deps.get_current_user)
) -> List[SafetyTraining]:
    """
    안전 교육 기록 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:safety_training"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="안전 교육 기록 조회 권한이 없습니다"
        )
    
    filters = SafetyTrainingFilter(
        worker_id=worker_id,
        training_date_from=training_date_from,
        training_date_to=training_date_to,
        training_type=training_type,
        passed=passed
    )
    trainings = labor_crud.get_safety_trainings(
        db=db,
        skip=skip,
        limit=limit,
        filters=filters.dict(exclude_none=True)
    )
    return trainings

@router.get("/safety-trainings/{training_id}", response_model=SafetyTraining)
def read_safety_training(
    *,
    db: Session = Depends(deps.get_db),
    training_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> SafetyTraining:
    """
    특정 안전 교육 기록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:safety_training"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="안전 교육 기록 조회 권한이 없습니다"
        )
    
    training = labor_crud.get_safety_training(db=db, training_id=training_id)
    if not training:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="안전 교육 기록을 찾을 수 없습니다"
        )
    return training

@router.put("/safety-trainings/{training_id}", response_model=SafetyTraining)
def update_safety_training(
    *,
    db: Session = Depends(deps.get_db),
    training_id: int,
    training_in: SafetyTrainingUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> SafetyTraining:
    """
    안전 교육 기록을 업데이트합니다.
    """
    if not check_permissions(current_user, ["update:safety_training"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="안전 교육 기록 수정 권한이 없습니다"
        )
    
    training = labor_crud.get_safety_training(db=db, training_id=training_id)
    if not training:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="안전 교육 기록을 찾을 수 없습니다"
        )
    
    training = labor_crud.update_safety_training(
        db=db,
        training_id=training_id,
        training=training_in
    )
    return training

@router.delete("/safety-trainings/{training_id}")
def delete_safety_training(
    *,
    db: Session = Depends(deps.get_db),
    training_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> dict:
    """
    안전 교육 기록을 삭제합니다.
    """
    if not check_permissions(current_user, ["delete:safety_training"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="안전 교육 기록 삭제 권한이 없습니다"
        )
    
    training = labor_crud.get_safety_training(db=db, training_id=training_id)
    if not training:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="안전 교육 기록을 찾을 수 없습니다"
        )
    
    labor_crud.delete_safety_training(db=db, training_id=training_id)
    return {"message": "안전 교육 기록이 삭제되었습니다"}

# 자격증 관리
@router.post("/certifications", response_model=Certification)
def create_certification(
    *,
    db: Session = Depends(deps.get_db),
    certification_in: CertificationCreate,
    current_user: User = Depends(deps.get_current_user)
) -> Certification:
    """
    새로운 자격증 기록을 생성합니다.
    """
    if not check_permissions(current_user, ["create:certification"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="자격증 기록 생성 권한이 없습니다"
        )
    
    certification = labor_crud.create_certification(
        db=db,
        certification=certification_in,
        creator_id=current_user.id
    )
    return certification

@router.get("/certifications", response_model=List[Certification])
def read_certifications(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    worker_id: Optional[int] = None,
    name: Optional[str] = None,
    status: Optional[str] = None,
    expiry_date_from: Optional[datetime] = None,
    expiry_date_to: Optional[datetime] = None,
    current_user: User = Depends(deps.get_current_user)
) -> List[Certification]:
    """
    자격증 기록 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:certification"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="자격증 기록 조회 권한이 없습니다"
        )
    
    filters = CertificationFilter(
        worker_id=worker_id,
        name=name,
        status=status,
        expiry_date_from=expiry_date_from,
        expiry_date_to=expiry_date_to
    )
    certifications = labor_crud.get_certifications(
        db=db,
        skip=skip,
        limit=limit,
        filters=filters.dict(exclude_none=True)
    )
    return certifications

@router.get("/certifications/{certification_id}", response_model=Certification)
def read_certification(
    *,
    db: Session = Depends(deps.get_db),
    certification_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> Certification:
    """
    특정 자격증 기록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:certification"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="자격증 기록 조회 권한이 없습니다"
        )
    
    certification = labor_crud.get_certification(db=db, certification_id=certification_id)
    if not certification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="자격증 기록을 찾을 수 없습니다"
        )
    return certification

@router.put("/certifications/{certification_id}", response_model=Certification)
def update_certification(
    *,
    db: Session = Depends(deps.get_db),
    certification_id: int,
    certification_in: CertificationUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> Certification:
    """
    자격증 기록을 업데이트합니다.
    """
    if not check_permissions(current_user, ["update:certification"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="자격증 기록 수정 권한이 없습니다"
        )
    
    certification = labor_crud.get_certification(db=db, certification_id=certification_id)
    if not certification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="자격증 기록을 찾을 수 없습니다"
        )
    
    certification = labor_crud.update_certification(
        db=db,
        certification_id=certification_id,
        certification=certification_in
    )
    return certification

@router.delete("/certifications/{certification_id}")
def delete_certification(
    *,
    db: Session = Depends(deps.get_db),
    certification_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> dict:
    """
    자격증 기록을 삭제합니다.
    """
    if not check_permissions(current_user, ["delete:certification"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="자격증 기록 삭제 권한이 없습니다"
        )
    
    certification = labor_crud.get_certification(db=db, certification_id=certification_id)
    if not certification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="자격증 기록을 찾을 수 없습니다"
        )
    
    labor_crud.delete_certification(db=db, certification_id=certification_id)
    return {"message": "자격증 기록이 삭제되었습니다"}

# 급여 관리
@router.post("/payroll", response_model=PayrollRecord)
def create_payroll_record(
    *,
    db: Session = Depends(deps.get_db),
    payroll_in: PayrollRecordCreate,
    current_user: User = Depends(deps.get_current_user)
) -> PayrollRecord:
    """
    새로운 급여 기록을 생성합니다.
    """
    if not check_permissions(current_user, ["create:payroll"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="급여 기록 생성 권한이 없습니다"
        )
    
    payroll = labor_crud.create_payroll_record(
        db=db,
        payroll=payroll_in,
        creator_id=current_user.id
    )
    return payroll

@router.get("/payroll", response_model=List[PayrollRecord])
def read_payroll_records(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    worker_id: Optional[int] = None,
    payment_date_from: Optional[datetime] = None,
    payment_date_to: Optional[datetime] = None,
    status: Optional[str] = None,
    current_user: User = Depends(deps.get_current_user)
) -> List[PayrollRecord]:
    """
    급여 기록 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:payroll"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="급여 기록 조회 권한이 없습니다"
        )
    
    filters = PayrollFilter(
        worker_id=worker_id,
        payment_date_from=payment_date_from,
        payment_date_to=payment_date_to,
        status=status
    )
    payroll_records = labor_crud.get_payroll_records(
        db=db,
        skip=skip,
        limit=limit,
        filters=filters.dict(exclude_none=True)
    )
    return payroll_records

@router.get("/payroll/{payroll_id}", response_model=PayrollRecord)
def read_payroll_record(
    *,
    db: Session = Depends(deps.get_db),
    payroll_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> PayrollRecord:
    """
    특정 급여 기록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:payroll"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="급여 기록 조회 권한이 없습니다"
        )
    
    payroll = labor_crud.get_payroll_record(db=db, payroll_id=payroll_id)
    if not payroll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="급여 기록을 찾을 수 없습니다"
        )
    return payroll

@router.put("/payroll/{payroll_id}", response_model=PayrollRecord)
def update_payroll_record(
    *,
    db: Session = Depends(deps.get_db),
    payroll_id: int,
    payroll_in: PayrollRecordUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> PayrollRecord:
    """
    급여 기록을 업데이트합니다.
    """
    if not check_permissions(current_user, ["update:payroll"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="급여 기록 수정 권한이 없습니다"
        )
    
    payroll = labor_crud.get_payroll_record(db=db, payroll_id=payroll_id)
    if not payroll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="급여 기록을 찾을 수 없습니다"
        )
    
    payroll = labor_crud.update_payroll_record(
        db=db,
        payroll_id=payroll_id,
        payroll=payroll_in
    )
    return payroll

@router.delete("/payroll/{payroll_id}")
def delete_payroll_record(
    *,
    db: Session = Depends(deps.get_db),
    payroll_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> dict:
    """
    급여 기록을 삭제합니다.
    """
    if not check_permissions(current_user, ["delete:payroll"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="급여 기록 삭제 권한이 없습니다"
        )
    
    payroll = labor_crud.get_payroll_record(db=db, payroll_id=payroll_id)
    if not payroll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="급여 기록을 찾을 수 없습니다"
        )
    
    labor_crud.delete_payroll_record(db=db, payroll_id=payroll_id)
    return {"message": "급여 기록이 삭제되었습니다"} 