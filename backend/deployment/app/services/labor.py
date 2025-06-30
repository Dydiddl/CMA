from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from ..models.labor import Worker, WorkRecord, Salary, WorkerDocument
from ..schemas.labor import (
    WorkerCreate,
    WorkerUpdate,
    WorkRecordCreate,
    SalaryCreate,
    WorkerDocumentCreate
)

def create_worker(db: Session, worker: WorkerCreate) -> Worker:
    """새로운 인력을 등록합니다."""
    db_worker = Worker(**worker.dict())
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return db_worker

def get_workers(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None
) -> List[Worker]:
    """인력 목록을 조회합니다."""
    query = db.query(Worker)
    if status:
        query = query.filter(Worker.status == status)
    return query.offset(skip).limit(limit).all()

def get_worker(db: Session, worker_id: int) -> Optional[Worker]:
    """특정 인력의 정보를 조회합니다."""
    return db.query(Worker).filter(Worker.id == worker_id).first()

def update_worker(
    db: Session,
    worker_id: int,
    worker: WorkerUpdate
) -> Optional[Worker]:
    """인력 정보를 업데이트합니다."""
    db_worker = get_worker(db, worker_id)
    if db_worker:
        for key, value in worker.dict(exclude_unset=True).items():
            setattr(db_worker, key, value)
        db.commit()
        db.refresh(db_worker)
    return db_worker

def delete_worker(db: Session, worker_id: int) -> bool:
    """인력을 삭제합니다."""
    db_worker = get_worker(db, worker_id)
    if db_worker:
        db.delete(db_worker)
        db.commit()
        return True
    return False

def create_work_record(
    db: Session,
    worker_id: int,
    record: WorkRecordCreate
) -> WorkRecord:
    """근무 기록을 생성합니다."""
    db_record = WorkRecord(**record.dict(), worker_id=worker_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_work_records(
    db: Session,
    worker_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> List[WorkRecord]:
    """인력의 근무 기록을 조회합니다."""
    query = db.query(WorkRecord).filter(WorkRecord.worker_id == worker_id)
    if start_date:
        query = query.filter(WorkRecord.date >= start_date)
    if end_date:
        query = query.filter(WorkRecord.date <= end_date)
    return query.all()

def create_salary(
    db: Session,
    worker_id: int,
    salary: SalaryCreate
) -> Salary:
    """급여 정보를 생성합니다."""
    db_salary = Salary(**salary.dict(), worker_id=worker_id)
    db.add(db_salary)
    db.commit()
    db.refresh(db_salary)
    return db_salary

def get_salaries(
    db: Session,
    worker_id: int,
    year: Optional[int] = None,
    month: Optional[int] = None
) -> List[Salary]:
    """인력의 급여 정보를 조회합니다."""
    query = db.query(Salary).filter(Salary.worker_id == worker_id)
    if year:
        query = query.filter(Salary.year == year)
    if month:
        query = query.filter(Salary.month == month)
    return query.all()

def create_worker_document(
    db: Session,
    worker_id: int,
    document: WorkerDocumentCreate
) -> WorkerDocument:
    """인력 문서를 생성합니다."""
    db_document = WorkerDocument(**document.dict(), worker_id=worker_id)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_worker_documents(
    db: Session,
    worker_id: int
) -> List[WorkerDocument]:
    """인력의 모든 문서를 조회합니다."""
    return db.query(WorkerDocument).filter(
        WorkerDocument.worker_id == worker_id
    ).all() 