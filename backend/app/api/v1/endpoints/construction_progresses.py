from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from datetime import datetime

from app.api import deps
from app.core.permissions import check_permissions
from app.models.user import User
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
from app.services.file_service import FileService

router = APIRouter()
file_service = FileService()

# 공사진행 CRUD
@router.post("/", response_model=ConstructionProgress)
def create_progress(
    *,
    db: Session = Depends(deps.get_db),
    progress_in: ConstructionProgressCreate,
    current_user: User = Depends(deps.get_current_user)
) -> ConstructionProgress:
    """
    새로운 공사진행 기록을 생성합니다.
    """
    if not check_permissions(current_user, ["create:construction_progress"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="공사진행 기록 생성 권한이 없습니다"
        )
    
    progress = crud.create_progress(db=db, progress=progress_in, created_by=current_user.id)
    return progress

@router.get("/{progress_id}", response_model=ConstructionProgress)
def read_progress(
    *,
    db: Session = Depends(deps.get_db),
    progress_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> ConstructionProgress:
    """
    ID로 공사진행 기록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:construction_progress"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="공사진행 기록 조회 권한이 없습니다"
        )
    
    progress = crud.get_progress(db=db, progress_id=progress_id)
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="공사진행 기록을 찾을 수 없습니다"
        )
    return progress

@router.get("/", response_model=List[ConstructionProgress])
def read_progresses(
    *,
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
    progress_percentage_max: Optional[float] = None,
    current_user: User = Depends(deps.get_current_user)
) -> List[ConstructionProgress]:
    """
    필터 조건에 맞는 공사진행 기록 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:construction_progress"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="공사진행 기록 조회 권한이 없습니다"
        )
    
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
    progress_in: ConstructionProgressUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> ConstructionProgress:
    """
    공사진행 기록을 업데이트합니다.
    """
    if not check_permissions(current_user, ["update:construction_progress"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="공사진행 기록 수정 권한이 없습니다"
        )
    
    progress = crud.get_progress(db=db, progress_id=progress_id)
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="공사진행 기록을 찾을 수 없습니다"
        )
    progress = crud.update_progress(db=db, progress_id=progress_id, progress=progress_in, updated_by=current_user.id)
    return progress

@router.delete("/{progress_id}")
def delete_progress(
    *,
    db: Session = Depends(deps.get_db),
    progress_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> dict:
    """
    공사진행 기록을 삭제합니다.
    """
    if not check_permissions(current_user, ["delete:construction_progress"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="공사진행 기록 삭제 권한이 없습니다"
        )
    
    progress = crud.get_progress(db=db, progress_id=progress_id)
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="공사진행 기록을 찾을 수 없습니다"
        )
    crud.delete_progress(db=db, progress_id=progress_id)
    return {"message": "공사진행 기록이 삭제되었습니다"}

# 공사 사진 CRUD
@router.post("/{progress_id}/photos", response_model=ConstructionPhoto)
async def create_photo(
    *,
    db: Session = Depends(deps.get_db),
    progress_id: int,
    file: UploadFile = File(...),
    description: Optional[str] = None,
    current_user: User = Depends(deps.get_current_user)
) -> ConstructionPhoto:
    """
    새로운 공사 사진을 추가합니다.
    """
    if not check_permissions(current_user, ["create:construction_photo"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="공사 사진 업로드 권한이 없습니다"
        )
    
    # 파일 저장
    file_url, file_name, file_size = await file_service.save_file(
        file=file,
        document_type="construction",
        document_id=progress_id
    )
    
    photo_in = ConstructionPhotoCreate(
        photo_url=file_url,
        file_name=file_name,
        file_size=file_size,
        description=description
    )
    photo = crud.create_photo(db=db, photo=photo_in, progress_id=progress_id, uploaded_by=current_user.id)
    return photo

@router.get("/{progress_id}/photos", response_model=List[ConstructionPhoto])
def read_photos(
    *,
    db: Session = Depends(deps.get_db),
    progress_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> List[ConstructionPhoto]:
    """
    공사진행 기록의 사진 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:construction_photo"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="공사 사진 조회 권한이 없습니다"
        )
    
    photos = crud.get_photos_by_progress(db=db, progress_id=progress_id, skip=skip, limit=limit)
    return photos

@router.delete("/photos/{photo_id}")
def delete_photo(
    *,
    db: Session = Depends(deps.get_db),
    photo_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> dict:
    """
    공사 사진을 삭제합니다.
    """
    if not check_permissions(current_user, ["delete:construction_photo"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="공사 사진 삭제 권한이 없습니다"
        )
    
    photo = crud.get_photo(db=db, photo_id=photo_id)
    if not photo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="공사 사진을 찾을 수 없습니다"
        )
    crud.delete_photo(db=db, photo_id=photo_id)
    return {"message": "공사 사진이 삭제되었습니다"}

# 안전 점검 CRUD
@router.post("/{progress_id}/safety-checks", response_model=SafetyCheck)
def create_safety_check(
    *,
    db: Session = Depends(deps.get_db),
    progress_id: int,
    safety_check_in: SafetyCheckCreate,
    current_user: User = Depends(deps.get_current_user)
) -> SafetyCheck:
    """
    새로운 안전 점검 기록을 추가합니다.
    """
    if not check_permissions(current_user, ["create:safety_check"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="안전 점검 기록 생성 권한이 없습니다"
        )
    
    safety_check = crud.create_safety_check(db=db, safety_check=safety_check_in, progress_id=progress_id, created_by=current_user.id)
    return safety_check

@router.get("/{progress_id}/safety-checks", response_model=List[SafetyCheck])
def read_safety_checks(
    *,
    db: Session = Depends(deps.get_db),
    progress_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> List[SafetyCheck]:
    """
    공사진행 기록의 안전 점검 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:safety_check"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="안전 점검 기록 조회 권한이 없습니다"
        )
    
    safety_checks = crud.get_safety_checks_by_progress(db=db, progress_id=progress_id, skip=skip, limit=limit)
    return safety_checks

@router.delete("/safety-checks/{safety_check_id}")
def delete_safety_check(
    *,
    db: Session = Depends(deps.get_db),
    safety_check_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> dict:
    """
    안전 점검 기록을 삭제합니다.
    """
    if not check_permissions(current_user, ["delete:safety_check"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="안전 점검 기록 삭제 권한이 없습니다"
        )
    
    safety_check = crud.get_safety_check(db=db, safety_check_id=safety_check_id)
    if not safety_check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="안전 점검 기록을 찾을 수 없습니다"
        )
    crud.delete_safety_check(db=db, safety_check_id=safety_check_id)
    return {"message": "안전 점검 기록이 삭제되었습니다"}

# 품질 점검 CRUD
@router.post("/{progress_id}/quality-checks", response_model=QualityCheck)
def create_quality_check(
    *,
    db: Session = Depends(deps.get_db),
    progress_id: int,
    quality_check_in: QualityCheckCreate,
    current_user: User = Depends(deps.get_current_user)
) -> QualityCheck:
    """
    새로운 품질 점검 기록을 추가합니다.
    """
    if not check_permissions(current_user, ["create:quality_check"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="품질 점검 기록 생성 권한이 없습니다"
        )
    
    quality_check = crud.create_quality_check(db=db, quality_check=quality_check_in, progress_id=progress_id, created_by=current_user.id)
    return quality_check

@router.get("/{progress_id}/quality-checks", response_model=List[QualityCheck])
def read_quality_checks(
    *,
    db: Session = Depends(deps.get_db),
    progress_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> List[QualityCheck]:
    """
    공사진행 기록의 품질 점검 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:quality_check"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="품질 점검 기록 조회 권한이 없습니다"
        )
    
    quality_checks = crud.get_quality_checks_by_progress(db=db, progress_id=progress_id, skip=skip, limit=limit)
    return quality_checks

@router.delete("/quality-checks/{quality_check_id}")
def delete_quality_check(
    *,
    db: Session = Depends(deps.get_db),
    quality_check_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> dict:
    """
    품질 점검 기록을 삭제합니다.
    """
    if not check_permissions(current_user, ["delete:quality_check"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="품질 점검 기록 삭제 권한이 없습니다"
        )
    
    quality_check = crud.get_quality_check(db=db, quality_check_id=quality_check_id)
    if not quality_check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="품질 점검 기록을 찾을 수 없습니다"
        )
    crud.delete_quality_check(db=db, quality_check_id=quality_check_id)
    return {"message": "품질 점검 기록이 삭제되었습니다"} 