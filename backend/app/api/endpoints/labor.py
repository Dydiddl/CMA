from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.api import deps
from app.crud import labor as crud
from app.schemas.labor import (
    Worker, WorkerCreate, WorkerUpdate, WorkerFilter,
    AttendanceRecord, AttendanceRecordCreate, AttendanceRecordUpdate, AttendanceFilter,
    SafetyTraining, SafetyTrainingCreate, SafetyTrainingUpdate, SafetyTrainingFilter,
    Certification, CertificationCreate, CertificationUpdate, CertificationFilter,
    PayrollRecord, PayrollRecordCreate, PayrollRecordUpdate, PayrollFilter
)

router = APIRouter()

# Worker 엔드포인트
@router.post("/workers", response_model=Worker)
def create_worker(
    *,
    db: Session = Depends(deps.get_db),
    worker_in: WorkerCreate
) -> Worker:
    """
    새로운 근로자를 등록합니다.
    """
    worker = crud.create_worker(db=db, worker=worker_in)
    return worker

@router.get("/workers/{worker_id}", response_model=Worker)
def get_worker(
    *,
    db: Session = Depends(deps.get_db),
    worker_id: int
) -> Worker:
    """
    ID로 근로자 정보를 조회합니다.
    """
    worker = crud.get_worker(db=db, worker_id=worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="근로자를 찾을 수 없습니다.")
    return worker

@router.get("/workers", response_model=List[Worker])
def get_workers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    worker_type: Optional[str] = None,
    status: Optional[str] = None,
    hire_date_from: Optional[datetime] = None,
    hire_date_to: Optional[datetime] = None
) -> List[Worker]:
    """
    필터 조건에 맞는 근로자 목록을 조회합니다.
    """
    filters = WorkerFilter(
        name=name,
        worker_type=worker_type,
        status=status,
        hire_date_from=hire_date_from,
        hire_date_to=hire_date_to
    )
    workers = crud.get_workers(db=db, skip=skip, limit=limit, filters=filters)
    return workers

@router.put("/workers/{worker_id}", response_model=Worker)
def update_worker(
    *,
    db: Session = Depends(deps.get_db),
    worker_id: int,
    worker_in: WorkerUpdate
) -> Worker:
    """
    근로자 정보를 업데이트합니다.
    """
    worker = crud.get_worker(db=db, worker_id=worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="근로자를 찾을 수 없습니다.")
    worker = crud.update_worker(db=db, worker_id=worker_id, worker=worker_in)
    return worker

@router.delete("/workers/{worker_id}")
def delete_worker(
    *,
    db: Session = Depends(deps.get_db),
    worker_id: int
) -> dict:
    """
    근로자 정보를 삭제합니다.
    """
    worker = crud.get_worker(db=db, worker_id=worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="근로자를 찾을 수 없습니다.")
    crud.delete_worker(db=db, worker_id=worker_id)
    return {"message": "근로자 정보가 삭제되었습니다."}

# AttendanceRecord 엔드포인트
@router.post("/attendance", response_model=AttendanceRecord)
def create_attendance_record(
    *,
    db: Session = Depends(deps.get_db),
    attendance_in: AttendanceRecordCreate
) -> AttendanceRecord:
    """
    새로운 근태 기록을 생성합니다.
    """
    attendance = crud.create_attendance_record(db=db, attendance=attendance_in)
    return attendance

@router.get("/attendance/{attendance_id}", response_model=AttendanceRecord)
def get_attendance_record(
    *,
    db: Session = Depends(deps.get_db),
    attendance_id: int
) -> AttendanceRecord:
    """
    ID로 근태 기록을 조회합니다.
    """
    attendance = crud.get_attendance_record(db=db, attendance_id=attendance_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="근태 기록을 찾을 수 없습니다.")
    return attendance

@router.get("/attendance", response_model=List[AttendanceRecord])
def get_attendance_records(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    worker_id: Optional[int] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    status: Optional[str] = None
) -> List[AttendanceRecord]:
    """
    필터 조건에 맞는 근태 기록 목록을 조회합니다.
    """
    filters = AttendanceFilter(
        worker_id=worker_id,
        date_from=date_from,
        date_to=date_to,
        status=status
    )
    attendance_records = crud.get_attendance_records(db=db, skip=skip, limit=limit, filters=filters)
    return attendance_records

@router.put("/attendance/{attendance_id}", response_model=AttendanceRecord)
def update_attendance_record(
    *,
    db: Session = Depends(deps.get_db),
    attendance_id: int,
    attendance_in: AttendanceRecordUpdate
) -> AttendanceRecord:
    """
    근태 기록을 업데이트합니다.
    """
    attendance = crud.get_attendance_record(db=db, attendance_id=attendance_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="근태 기록을 찾을 수 없습니다.")
    attendance = crud.update_attendance_record(db=db, attendance_id=attendance_id, attendance=attendance_in)
    return attendance

@router.delete("/attendance/{attendance_id}")
def delete_attendance_record(
    *,
    db: Session = Depends(deps.get_db),
    attendance_id: int
) -> dict:
    """
    근태 기록을 삭제합니다.
    """
    attendance = crud.get_attendance_record(db=db, attendance_id=attendance_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="근태 기록을 찾을 수 없습니다.")
    crud.delete_attendance_record(db=db, attendance_id=attendance_id)
    return {"message": "근태 기록이 삭제되었습니다."}

# SafetyTraining 엔드포인트
@router.post("/safety-trainings", response_model=SafetyTraining)
def create_safety_training(
    *,
    db: Session = Depends(deps.get_db),
    training_in: SafetyTrainingCreate
) -> SafetyTraining:
    """
    새로운 안전 교육 기록을 생성합니다.
    """
    training = crud.create_safety_training(db=db, training=training_in)
    return training

@router.get("/safety-trainings/{training_id}", response_model=SafetyTraining)
def get_safety_training(
    *,
    db: Session = Depends(deps.get_db),
    training_id: int
) -> SafetyTraining:
    """
    ID로 안전 교육 기록을 조회합니다.
    """
    training = crud.get_safety_training(db=db, training_id=training_id)
    if not training:
        raise HTTPException(status_code=404, detail="안전 교육 기록을 찾을 수 없습니다.")
    return training

@router.get("/safety-trainings", response_model=List[SafetyTraining])
def get_safety_trainings(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    worker_id: Optional[int] = None,
    training_date_from: Optional[datetime] = None,
    training_date_to: Optional[datetime] = None,
    training_type: Optional[str] = None,
    passed: Optional[bool] = None
) -> List[SafetyTraining]:
    """
    필터 조건에 맞는 안전 교육 기록 목록을 조회합니다.
    """
    filters = SafetyTrainingFilter(
        worker_id=worker_id,
        training_date_from=training_date_from,
        training_date_to=training_date_to,
        training_type=training_type,
        passed=passed
    )
    trainings = crud.get_safety_trainings(db=db, skip=skip, limit=limit, filters=filters)
    return trainings

@router.put("/safety-trainings/{training_id}", response_model=SafetyTraining)
def update_safety_training(
    *,
    db: Session = Depends(deps.get_db),
    training_id: int,
    training_in: SafetyTrainingUpdate
) -> SafetyTraining:
    """
    안전 교육 기록을 업데이트합니다.
    """
    training = crud.get_safety_training(db=db, training_id=training_id)
    if not training:
        raise HTTPException(status_code=404, detail="안전 교육 기록을 찾을 수 없습니다.")
    training = crud.update_safety_training(db=db, training_id=training_id, training=training_in)
    return training

@router.delete("/safety-trainings/{training_id}")
def delete_safety_training(
    *,
    db: Session = Depends(deps.get_db),
    training_id: int
) -> dict:
    """
    안전 교육 기록을 삭제합니다.
    """
    training = crud.get_safety_training(db=db, training_id=training_id)
    if not training:
        raise HTTPException(status_code=404, detail="안전 교육 기록을 찾을 수 없습니다.")
    crud.delete_safety_training(db=db, training_id=training_id)
    return {"message": "안전 교육 기록이 삭제되었습니다."}

# Certification 엔드포인트
@router.post("/certifications", response_model=Certification)
def create_certification(
    *,
    db: Session = Depends(deps.get_db),
    certification_in: CertificationCreate
) -> Certification:
    """
    새로운 자격증 기록을 생성합니다.
    """
    certification = crud.create_certification(db=db, certification=certification_in)
    return certification

@router.get("/certifications/{certification_id}", response_model=Certification)
def get_certification(
    *,
    db: Session = Depends(deps.get_db),
    certification_id: int
) -> Certification:
    """
    ID로 자격증 기록을 조회합니다.
    """
    certification = crud.get_certification(db=db, certification_id=certification_id)
    if not certification:
        raise HTTPException(status_code=404, detail="자격증 기록을 찾을 수 없습니다.")
    return certification

@router.get("/certifications", response_model=List[Certification])
def get_certifications(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    worker_id: Optional[int] = None,
    name: Optional[str] = None,
    status: Optional[str] = None,
    expiry_date_from: Optional[datetime] = None,
    expiry_date_to: Optional[datetime] = None
) -> List[Certification]:
    """
    필터 조건에 맞는 자격증 기록 목록을 조회합니다.
    """
    filters = CertificationFilter(
        worker_id=worker_id,
        name=name,
        status=status,
        expiry_date_from=expiry_date_from,
        expiry_date_to=expiry_date_to
    )
    certifications = crud.get_certifications(db=db, skip=skip, limit=limit, filters=filters)
    return certifications

@router.put("/certifications/{certification_id}", response_model=Certification)
def update_certification(
    *,
    db: Session = Depends(deps.get_db),
    certification_id: int,
    certification_in: CertificationUpdate
) -> Certification:
    """
    자격증 기록을 업데이트합니다.
    """
    certification = crud.get_certification(db=db, certification_id=certification_id)
    if not certification:
        raise HTTPException(status_code=404, detail="자격증 기록을 찾을 수 없습니다.")
    certification = crud.update_certification(db=db, certification_id=certification_id, certification=certification_in)
    return certification

@router.delete("/certifications/{certification_id}")
def delete_certification(
    *,
    db: Session = Depends(deps.get_db),
    certification_id: int
) -> dict:
    """
    자격증 기록을 삭제합니다.
    """
    certification = crud.get_certification(db=db, certification_id=certification_id)
    if not certification:
        raise HTTPException(status_code=404, detail="자격증 기록을 찾을 수 없습니다.")
    crud.delete_certification(db=db, certification_id=certification_id)
    return {"message": "자격증 기록이 삭제되었습니다."}

# PayrollRecord 엔드포인트
@router.post("/payroll", response_model=PayrollRecord)
def create_payroll_record(
    *,
    db: Session = Depends(deps.get_db),
    payroll_in: PayrollRecordCreate
) -> PayrollRecord:
    """
    새로운 급여 기록을 생성합니다.
    """
    payroll = crud.create_payroll_record(db=db, payroll=payroll_in)
    return payroll

@router.get("/payroll/{payroll_id}", response_model=PayrollRecord)
def get_payroll_record(
    *,
    db: Session = Depends(deps.get_db),
    payroll_id: int
) -> PayrollRecord:
    """
    ID로 급여 기록을 조회합니다.
    """
    payroll = crud.get_payroll_record(db=db, payroll_id=payroll_id)
    if not payroll:
        raise HTTPException(status_code=404, detail="급여 기록을 찾을 수 없습니다.")
    return payroll

@router.get("/payroll", response_model=List[PayrollRecord])
def get_payroll_records(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    worker_id: Optional[int] = None,
    payment_date_from: Optional[datetime] = None,
    payment_date_to: Optional[datetime] = None,
    status: Optional[str] = None
) -> List[PayrollRecord]:
    """
    필터 조건에 맞는 급여 기록 목록을 조회합니다.
    """
    filters = PayrollFilter(
        worker_id=worker_id,
        payment_date_from=payment_date_from,
        payment_date_to=payment_date_to,
        status=status
    )
    payroll_records = crud.get_payroll_records(db=db, skip=skip, limit=limit, filters=filters)
    return payroll_records

@router.put("/payroll/{payroll_id}", response_model=PayrollRecord)
def update_payroll_record(
    *,
    db: Session = Depends(deps.get_db),
    payroll_id: int,
    payroll_in: PayrollRecordUpdate
) -> PayrollRecord:
    """
    급여 기록을 업데이트합니다.
    """
    payroll = crud.get_payroll_record(db=db, payroll_id=payroll_id)
    if not payroll:
        raise HTTPException(status_code=404, detail="급여 기록을 찾을 수 없습니다.")
    payroll = crud.update_payroll_record(db=db, payroll_id=payroll_id, payroll=payroll_in)
    return payroll

@router.delete("/payroll/{payroll_id}")
def delete_payroll_record(
    *,
    db: Session = Depends(deps.get_db),
    payroll_id: int
) -> dict:
    """
    급여 기록을 삭제합니다.
    """
    payroll = crud.get_payroll_record(db=db, payroll_id=payroll_id)
    if not payroll:
        raise HTTPException(status_code=404, detail="급여 기록을 찾을 수 없습니다.")
    crud.delete_payroll_record(db=db, payroll_id=payroll_id)
    return {"message": "급여 기록이 삭제되었습니다."} 