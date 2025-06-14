from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.core.permissions import check_permissions
from app.models.user import User
from app.schemas.labor import (
    WorkerCreate, WorkerUpdate, Worker,
    SafetyTrainingCreate, SafetyTraining,
    CertificationCreate, Certification
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
    department_id: Optional[int] = None,
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
    
    workers = labor_crud.get_workers(
        db=db,
        skip=skip,
        limit=limit,
        department_id=department_id
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