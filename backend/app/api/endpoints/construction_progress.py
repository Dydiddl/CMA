from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from datetime import datetime

from app.api import deps
from app.crud import construction_progress as crud
from app.schemas.construction_progress import (
    ConstructionProgress,
    ConstructionProgressCreate,
    ConstructionProgressUpdate,
    ConstructionProgressFilter,
    ConstructionPhoto,
    ConstructionPhotoCreate,
    SafetyCheck,
    SafetyCheckCreate,
    QualityCheck,
    QualityCheckCreate
)
from app.models.construction_progress import ProgressStatus

router = APIRouter()

# 공사진행 CRUD
@router.post("/", response_model=ConstructionProgress)
def create_progress(
    *,
    db: Session = Depends(deps.get_db),
    progress_in: ConstructionProgressCreate
) -> ConstructionProgress:
    """
    새로운 공사진행 기록을 생성합니다.
    """
    progress = crud.create_progress(db=db, progress=progress_in)
    return progress

@router.get("/{progress_id}", response_model=ConstructionProgress)
def get_progress(
    *,
    db: Session = Depends(deps.get_db),
    progress_id: int
) -> ConstructionProgress:
    """
    ID로 공사진행 기록을 조회합니다.
    """
    progress = crud.get_progress(db=db, progress_id=progress_id)
    if not progress:
        raise HTTPException(status_code=404, detail="공사진행 기록을 찾을 수 없습니다.")
    return progress

@router.get("/", response_model=List[ConstructionProgress])
def get_progresses(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    construction_id: Optional[int] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    status: Optional[ProgressStatus] = None,
    work_type: Optional[str] = None,
    work_area: Optional[str] = None,
    progress_percentage_min: Optional[float] = None,
    progress_percentage_max: Optional[float] = None
) -> List[ConstructionProgress]:
    """
    필터 조건에 맞는 공사진행 기록 목록을 조회합니다.
    """
    filters = ConstructionProgressFilter(
        construction_id=construction_id,
        date_from=date_from,
        date_to=date_to,
        status=status,
        work_type=work_type,
        work_area=work_area,
        progress_percentage_min=progress_percentage_min,
        progress_percentage_max=progress_percentage_max
    )
    progresses = crud.get_progresses(db=db, skip=skip, limit=limit, filters=filters)
    return progresses

@router.put("/{progress_id}", response_model=ConstructionProgress)
def update_progress(
    *,
    db: Session = Depends(deps.get_db),
    progress_id: int,
    progress_in: ConstructionProgressUpdate
) -> ConstructionProgress:
    """
    공사진행 기록을 업데이트합니다.
    """
    progress = crud.get_progress(db=db, progress_id=progress_id)
    if not progress:
        raise HTTPException(status_code=404, detail="공사진행 기록을 찾을 수 없습니다.")
    progress = crud.update_progress(db=db, progress_id=progress_id, progress=progress_in)
    return progress

@router.delete("/{progress_id}")
def delete_progress(
    *,
    db: Session = Depends(deps.get_db),
    progress_id: int
) -> dict:
    """
    공사진행 기록을 삭제합니다.
    """
    progress = crud.get_progress(db=db, progress_id=progress_id)
    if not progress:
        raise HTTPException(status_code=404, detail="공사진행 기록을 찾을 수 없습니다.")
    crud.delete_progress(db=db, progress_id=progress_id)
    return {"message": "공사진행 기록이 삭제되었습니다."}

# 공사 사진 CRUD
@router.post("/{progress_id}/photos", response_model=ConstructionPhoto)
async def create_photo(
    *,
    db: Session = Depends(deps.get_db),
    progress_id: int,
    file: UploadFile = File(...),
    description: Optional[str] = None
) -> ConstructionPhoto:
    """
    새로운 공사 사진을 추가합니다.
    """
    # TODO: 파일 업로드 처리 로직 구현
    photo_url = "temp_url"  # 실제 구현에서는 파일을 저장하고 URL을 반환
    photo_in = ConstructionPhotoCreate(
        photo_url=photo_url,
        description=description
    )
    photo = crud.create_photo(db=db, photo=photo_in, progress_id=progress_id)
    return photo

@router.get("/{progress_id}/photos", response_model=List[ConstructionPhoto])
def get_photos(
    *,
    db: Session = Depends(deps.get_db),
    progress_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[ConstructionPhoto]:
    """
    공사진행 기록의 사진 목록을 조회합니다.
    """
    photos = crud.get_photos_by_progress(db=db, progress_id=progress_id, skip=skip, limit=limit)
    return photos

@router.delete("/photos/{photo_id}")
def delete_photo(
    *,
    db: Session = Depends(deps.get_db),
    photo_id: int
) -> dict:
    """
    공사 사진을 삭제합니다.
    """
    photo = crud.get_photo(db=db, photo_id=photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="공사 사진을 찾을 수 없습니다.")
    crud.delete_photo(db=db, photo_id=photo_id)
    return {"message": "공사 사진이 삭제되었습니다."}

# 안전 점검 CRUD
@router.post("/{progress_id}/safety-checks", response_model=SafetyCheck)
def create_safety_check(
    *,
    db: Session = Depends(deps.get_db),
    progress_id: int,
    safety_check_in: SafetyCheckCreate
) -> SafetyCheck:
    """
    새로운 안전 점검 기록을 추가합니다.
    """
    safety_check = crud.create_safety_check(db=db, safety_check=safety_check_in, progress_id=progress_id)
    return safety_check

@router.get("/{progress_id}/safety-checks", response_model=List[SafetyCheck])
def get_safety_checks(
    *,
    db: Session = Depends(deps.get_db),
    progress_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[SafetyCheck]:
    """
    공사진행 기록의 안전 점검 목록을 조회합니다.
    """
    safety_checks = crud.get_safety_checks_by_progress(db=db, progress_id=progress_id, skip=skip, limit=limit)
    return safety_checks

@router.delete("/safety-checks/{safety_check_id}")
def delete_safety_check(
    *,
    db: Session = Depends(deps.get_db),
    safety_check_id: int
) -> dict:
    """
    안전 점검 기록을 삭제합니다.
    """
    safety_check = crud.get_safety_check(db=db, safety_check_id=safety_check_id)
    if not safety_check:
        raise HTTPException(status_code=404, detail="안전 점검 기록을 찾을 수 없습니다.")
    crud.delete_safety_check(db=db, safety_check_id=safety_check_id)
    return {"message": "안전 점검 기록이 삭제되었습니다."}

# 품질 점검 CRUD
@router.post("/{progress_id}/quality-checks", response_model=QualityCheck)
def create_quality_check(
    *,
    db: Session = Depends(deps.get_db),
    progress_id: int,
    quality_check_in: QualityCheckCreate
) -> QualityCheck:
    """
    새로운 품질 점검 기록을 추가합니다.
    """
    quality_check = crud.create_quality_check(db=db, quality_check=quality_check_in, progress_id=progress_id)
    return quality_check

@router.get("/{progress_id}/quality-checks", response_model=List[QualityCheck])
def get_quality_checks(
    *,
    db: Session = Depends(deps.get_db),
    progress_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[QualityCheck]:
    """
    공사진행 기록의 품질 점검 목록을 조회합니다.
    """
    quality_checks = crud.get_quality_checks_by_progress(db=db, progress_id=progress_id, skip=skip, limit=limit)
    return quality_checks

@router.delete("/quality-checks/{quality_check_id}")
def delete_quality_check(
    *,
    db: Session = Depends(deps.get_db),
    quality_check_id: int
) -> dict:
    """
    품질 점검 기록을 삭제합니다.
    """
    quality_check = crud.get_quality_check(db=db, quality_check_id=quality_check_id)
    if not quality_check:
        raise HTTPException(status_code=404, detail="품질 점검 기록을 찾을 수 없습니다.")
    crud.delete_quality_check(db=db, quality_check_id=quality_check_id)
    return {"message": "품질 점검 기록이 삭제되었습니다."} 