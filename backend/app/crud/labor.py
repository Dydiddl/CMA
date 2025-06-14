from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime

from app.models.labor import Worker, AttendanceRecord, SafetyTraining, Certification, PayrollRecord
from app.schemas.labor import (
    WorkerCreate, WorkerUpdate, WorkerFilter,
    AttendanceRecordCreate, AttendanceRecordUpdate, AttendanceFilter,
    SafetyTrainingCreate, SafetyTrainingUpdate, SafetyTrainingFilter,
    CertificationCreate, CertificationUpdate, CertificationFilter,
    PayrollRecordCreate, PayrollRecordUpdate, PayrollFilter
)

# Worker CRUD
def create_worker(db: Session, worker: WorkerCreate) -> Worker:
    db_worker = Worker(**worker.dict())
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return db_worker

def get_worker(db: Session, worker_id: int) -> Optional[Worker]:
    return db.query(Worker).filter(Worker.id == worker_id).first()

def get_workers(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    filters: Optional[WorkerFilter] = None
) -> List[Worker]:
    query = db.query(Worker)
    
    if filters:
        if filters.name:
            query = query.filter(Worker.name.ilike(f"%{filters.name}%"))
        if filters.worker_type:
            query = query.filter(Worker.worker_type == filters.worker_type)
        if filters.status:
            query = query.filter(Worker.status == filters.status)
        if filters.hire_date_from:
            query = query.filter(Worker.hire_date >= filters.hire_date_from)
        if filters.hire_date_to:
            query = query.filter(Worker.hire_date <= filters.hire_date_to)
    
    return query.offset(skip).limit(limit).all()

def update_worker(
    db: Session,
    worker_id: int,
    worker: WorkerUpdate
) -> Optional[Worker]:
    db_worker = get_worker(db, worker_id)
    if db_worker:
        update_data = worker.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_worker, field, value)
        db.commit()
        db.refresh(db_worker)
    return db_worker

def delete_worker(db: Session, worker_id: int) -> bool:
    db_worker = get_worker(db, worker_id)
    if db_worker:
        db.delete(db_worker)
        db.commit()
        return True
    return False

# AttendanceRecord CRUD
def create_attendance_record(
    db: Session,
    attendance: AttendanceRecordCreate
) -> AttendanceRecord:
    db_attendance = AttendanceRecord(**attendance.dict())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

def get_attendance_record(
    db: Session,
    attendance_id: int
) -> Optional[AttendanceRecord]:
    return db.query(AttendanceRecord).filter(AttendanceRecord.id == attendance_id).first()

def get_attendance_records(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    filters: Optional[AttendanceFilter] = None
) -> List[AttendanceRecord]:
    query = db.query(AttendanceRecord)
    
    if filters:
        if filters.worker_id:
            query = query.filter(AttendanceRecord.worker_id == filters.worker_id)
        if filters.date_from:
            query = query.filter(AttendanceRecord.date >= filters.date_from)
        if filters.date_to:
            query = query.filter(AttendanceRecord.date <= filters.date_to)
        if filters.status:
            query = query.filter(AttendanceRecord.status == filters.status)
    
    return query.offset(skip).limit(limit).all()

def update_attendance_record(
    db: Session,
    attendance_id: int,
    attendance: AttendanceRecordUpdate
) -> Optional[AttendanceRecord]:
    db_attendance = get_attendance_record(db, attendance_id)
    if db_attendance:
        update_data = attendance.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_attendance, field, value)
        db.commit()
        db.refresh(db_attendance)
    return db_attendance

def delete_attendance_record(db: Session, attendance_id: int) -> bool:
    db_attendance = get_attendance_record(db, attendance_id)
    if db_attendance:
        db.delete(db_attendance)
        db.commit()
        return True
    return False

# SafetyTraining CRUD
def create_safety_training(
    db: Session,
    training: SafetyTrainingCreate
) -> SafetyTraining:
    db_training = SafetyTraining(**training.dict())
    db.add(db_training)
    db.commit()
    db.refresh(db_training)
    return db_training

def get_safety_training(
    db: Session,
    training_id: int
) -> Optional[SafetyTraining]:
    return db.query(SafetyTraining).filter(SafetyTraining.id == training_id).first()

def get_safety_trainings(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    filters: Optional[SafetyTrainingFilter] = None
) -> List[SafetyTraining]:
    query = db.query(SafetyTraining)
    
    if filters:
        if filters.worker_id:
            query = query.filter(SafetyTraining.worker_id == filters.worker_id)
        if filters.training_date_from:
            query = query.filter(SafetyTraining.training_date >= filters.training_date_from)
        if filters.training_date_to:
            query = query.filter(SafetyTraining.training_date <= filters.training_date_to)
        if filters.training_type:
            query = query.filter(SafetyTraining.training_type == filters.training_type)
        if filters.passed is not None:
            query = query.filter(SafetyTraining.passed == filters.passed)
    
    return query.offset(skip).limit(limit).all()

def update_safety_training(
    db: Session,
    training_id: int,
    training: SafetyTrainingUpdate
) -> Optional[SafetyTraining]:
    db_training = get_safety_training(db, training_id)
    if db_training:
        update_data = training.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_training, field, value)
        db.commit()
        db.refresh(db_training)
    return db_training

def delete_safety_training(db: Session, training_id: int) -> bool:
    db_training = get_safety_training(db, training_id)
    if db_training:
        db.delete(db_training)
        db.commit()
        return True
    return False

# Certification CRUD
def create_certification(
    db: Session,
    certification: CertificationCreate
) -> Certification:
    db_certification = Certification(**certification.dict())
    db.add(db_certification)
    db.commit()
    db.refresh(db_certification)
    return db_certification

def get_certification(
    db: Session,
    certification_id: int
) -> Optional[Certification]:
    return db.query(Certification).filter(Certification.id == certification_id).first()

def get_certifications(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    filters: Optional[CertificationFilter] = None
) -> List[Certification]:
    query = db.query(Certification)
    
    if filters:
        if filters.worker_id:
            query = query.filter(Certification.worker_id == filters.worker_id)
        if filters.name:
            query = query.filter(Certification.name.ilike(f"%{filters.name}%"))
        if filters.status:
            query = query.filter(Certification.status == filters.status)
        if filters.expiry_date_from:
            query = query.filter(Certification.expiry_date >= filters.expiry_date_from)
        if filters.expiry_date_to:
            query = query.filter(Certification.expiry_date <= filters.expiry_date_to)
    
    return query.offset(skip).limit(limit).all()

def update_certification(
    db: Session,
    certification_id: int,
    certification: CertificationUpdate
) -> Optional[Certification]:
    db_certification = get_certification(db, certification_id)
    if db_certification:
        update_data = certification.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_certification, field, value)
        db.commit()
        db.refresh(db_certification)
    return db_certification

def delete_certification(db: Session, certification_id: int) -> bool:
    db_certification = get_certification(db, certification_id)
    if db_certification:
        db.delete(db_certification)
        db.commit()
        return True
    return False

# PayrollRecord CRUD
def create_payroll_record(
    db: Session,
    payroll: PayrollRecordCreate
) -> PayrollRecord:
    db_payroll = PayrollRecord(**payroll.dict())
    db.add(db_payroll)
    db.commit()
    db.refresh(db_payroll)
    return db_payroll

def get_payroll_record(
    db: Session,
    payroll_id: int
) -> Optional[PayrollRecord]:
    return db.query(PayrollRecord).filter(PayrollRecord.id == payroll_id).first()

def get_payroll_records(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    filters: Optional[PayrollFilter] = None
) -> List[PayrollRecord]:
    query = db.query(PayrollRecord)
    
    if filters:
        if filters.worker_id:
            query = query.filter(PayrollRecord.worker_id == filters.worker_id)
        if filters.payment_date_from:
            query = query.filter(PayrollRecord.payment_date >= filters.payment_date_from)
        if filters.payment_date_to:
            query = query.filter(PayrollRecord.payment_date <= filters.payment_date_to)
        if filters.status:
            query = query.filter(PayrollRecord.status == filters.status)
    
    return query.offset(skip).limit(limit).all()

def update_payroll_record(
    db: Session,
    payroll_id: int,
    payroll: PayrollRecordUpdate
) -> Optional[PayrollRecord]:
    db_payroll = get_payroll_record(db, payroll_id)
    if db_payroll:
        update_data = payroll.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_payroll, field, value)
        db.commit()
        db.refresh(db_payroll)
    return db_payroll

def delete_payroll_record(db: Session, payroll_id: int) -> bool:
    db_payroll = get_payroll_record(db, payroll_id)
    if db_payroll:
        db.delete(db_payroll)
        db.commit()
        return True
    return False 