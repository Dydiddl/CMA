from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime

from app.models.construction_progress import (
    ConstructionProgress,
    ConstructionPhoto,
    SafetyCheck,
    QualityCheck
)
from app.schemas.construction_progress import (
    ConstructionProgressCreate,
    ConstructionProgressUpdate,
    ConstructionProgressFilter,
    ConstructionPhotoCreate,
    SafetyCheckCreate,
    QualityCheckCreate
)

# 공사진행 CRUD
def create_progress(db: Session, progress: ConstructionProgressCreate) -> ConstructionProgress:
    """
    새로운 공사진행 기록을 생성합니다.
    """
    db_progress = ConstructionProgress(**progress.dict())
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress

def get_progress(db: Session, progress_id: int) -> Optional[ConstructionProgress]:
    """
    ID로 공사진행 기록을 조회합니다.
    """
    return db.query(ConstructionProgress).filter(ConstructionProgress.id == progress_id).first()

def get_progresses(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    filters: Optional[ConstructionProgressFilter] = None
) -> List[ConstructionProgress]:
    """
    필터 조건에 맞는 공사진행 기록 목록을 조회합니다.
    """
    query = db.query(ConstructionProgress)
    
    if filters:
        conditions = []
        
        if filters.construction_id:
            conditions.append(ConstructionProgress.construction_id == filters.construction_id)
        if filters.date_from:
            conditions.append(ConstructionProgress.date >= filters.date_from)
        if filters.date_to:
            conditions.append(ConstructionProgress.date <= filters.date_to)
        if filters.status:
            conditions.append(ConstructionProgress.status == filters.status)
        if filters.work_type:
            conditions.append(ConstructionProgress.work_type == filters.work_type)
        if filters.work_area:
            conditions.append(ConstructionProgress.work_area == filters.work_area)
        if filters.progress_percentage_min:
            conditions.append(ConstructionProgress.progress_percentage >= filters.progress_percentage_min)
        if filters.progress_percentage_max:
            conditions.append(ConstructionProgress.progress_percentage <= filters.progress_percentage_max)
            
        if conditions:
            query = query.filter(and_(*conditions))
    
    return query.offset(skip).limit(limit).all()

def update_progress(
    db: Session,
    progress_id: int,
    progress: ConstructionProgressUpdate
) -> Optional[ConstructionProgress]:
    """
    공사진행 기록을 업데이트합니다.
    """
    db_progress = get_progress(db, progress_id)
    if not db_progress:
        return None
        
    update_data = progress.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_progress, field, value)
    
    db_progress.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_progress)
    return db_progress

def delete_progress(db: Session, progress_id: int) -> bool:
    """
    공사진행 기록을 삭제합니다.
    """
    db_progress = get_progress(db, progress_id)
    if not db_progress:
        return False
        
    db.delete(db_progress)
    db.commit()
    return True

# 공사 사진 CRUD
def create_photo(db: Session, photo: ConstructionPhotoCreate, progress_id: int) -> ConstructionPhoto:
    """
    새로운 공사 사진을 추가합니다.
    """
    db_photo = ConstructionPhoto(**photo.dict(), progress_id=progress_id)
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo

def get_photo(db: Session, photo_id: int) -> Optional[ConstructionPhoto]:
    """
    ID로 공사 사진을 조회합니다.
    """
    return db.query(ConstructionPhoto).filter(ConstructionPhoto.id == photo_id).first()

def get_photos_by_progress(
    db: Session,
    progress_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[ConstructionPhoto]:
    """
    공사진행 기록의 사진 목록을 조회합니다.
    """
    return db.query(ConstructionPhoto)\
        .filter(ConstructionPhoto.progress_id == progress_id)\
        .offset(skip)\
        .limit(limit)\
        .all()

def delete_photo(db: Session, photo_id: int) -> bool:
    """
    공사 사진을 삭제합니다.
    """
    db_photo = get_photo(db, photo_id)
    if not db_photo:
        return False
        
    db.delete(db_photo)
    db.commit()
    return True

# 안전 점검 CRUD
def create_safety_check(
    db: Session,
    safety_check: SafetyCheckCreate,
    progress_id: int
) -> SafetyCheck:
    """
    새로운 안전 점검 기록을 추가합니다.
    """
    db_safety_check = SafetyCheck(**safety_check.dict(), progress_id=progress_id)
    db.add(db_safety_check)
    db.commit()
    db.refresh(db_safety_check)
    return db_safety_check

def get_safety_check(db: Session, safety_check_id: int) -> Optional[SafetyCheck]:
    """
    ID로 안전 점검 기록을 조회합니다.
    """
    return db.query(SafetyCheck).filter(SafetyCheck.id == safety_check_id).first()

def get_safety_checks_by_progress(
    db: Session,
    progress_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[SafetyCheck]:
    """
    공사진행 기록의 안전 점검 목록을 조회합니다.
    """
    return db.query(SafetyCheck)\
        .filter(SafetyCheck.progress_id == progress_id)\
        .offset(skip)\
        .limit(limit)\
        .all()

def delete_safety_check(db: Session, safety_check_id: int) -> bool:
    """
    안전 점검 기록을 삭제합니다.
    """
    db_safety_check = get_safety_check(db, safety_check_id)
    if not db_safety_check:
        return False
        
    db.delete(db_safety_check)
    db.commit()
    return True

# 품질 점검 CRUD
def create_quality_check(
    db: Session,
    quality_check: QualityCheckCreate,
    progress_id: int
) -> QualityCheck:
    """
    새로운 품질 점검 기록을 추가합니다.
    """
    db_quality_check = QualityCheck(**quality_check.dict(), progress_id=progress_id)
    db.add(db_quality_check)
    db.commit()
    db.refresh(db_quality_check)
    return db_quality_check

def get_quality_check(db: Session, quality_check_id: int) -> Optional[QualityCheck]:
    """
    ID로 품질 점검 기록을 조회합니다.
    """
    return db.query(QualityCheck).filter(QualityCheck.id == quality_check_id).first()

def get_quality_checks_by_progress(
    db: Session,
    progress_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[QualityCheck]:
    """
    공사진행 기록의 품질 점검 목록을 조회합니다.
    """
    return db.query(QualityCheck)\
        .filter(QualityCheck.progress_id == progress_id)\
        .offset(skip)\
        .limit(limit)\
        .all()

def delete_quality_check(db: Session, quality_check_id: int) -> bool:
    """
    품질 점검 기록을 삭제합니다.
    """
    db_quality_check = get_quality_check(db, quality_check_id)
    if not db_quality_check:
        return False
        
    db.delete(db_quality_check)
    db.commit()
    return True 