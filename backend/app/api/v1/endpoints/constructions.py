from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import construction as crud
from app.schemas.construction import (
    Construction,
    ConstructionCreate,
    ConstructionUpdate,
    ConstructionFilter
)
from app.models.construction import ConstructionStatus, ConstructionType

router = APIRouter()

@router.post("/", response_model=Construction)
def create_construction(
    *,
    db: Session = Depends(deps.get_db),
    construction_in: ConstructionCreate
) -> Construction:
    """
    새로운 공사를 생성합니다.
    """
    construction = crud.create_construction(db=db, construction=construction_in)
    return construction

@router.get("/{construction_id}", response_model=Construction)
def get_construction(
    *,
    db: Session = Depends(deps.get_db),
    construction_id: int
) -> Construction:
    """
    ID로 공사를 조회합니다.
    """
    construction = crud.get_construction(db=db, construction_id=construction_id)
    if not construction:
        raise HTTPException(status_code=404, detail="공사를 찾을 수 없습니다.")
    return construction

@router.get("/number/{construction_number}", response_model=Construction)
def get_construction_by_number(
    *,
    db: Session = Depends(deps.get_db),
    construction_number: str
) -> Construction:
    """
    공사번호로 공사를 조회합니다.
    """
    construction = crud.get_construction_by_number(db=db, construction_number=construction_number)
    if not construction:
        raise HTTPException(status_code=404, detail="공사를 찾을 수 없습니다.")
    return construction

@router.get("/", response_model=List[Construction])
def get_constructions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    construction_number: Optional[str] = None,
    type: Optional[ConstructionType] = None,
    status: Optional[ConstructionStatus] = None,
    location: Optional[str] = None,
    client_id: Optional[int] = None,
    contractor_id: Optional[int] = None,
    supervisor_id: Optional[int] = None,
    start_date_from: Optional[str] = None,
    start_date_to: Optional[str] = None,
    planned_end_date_from: Optional[str] = None,
    planned_end_date_to: Optional[str] = None,
    contract_amount_min: Optional[float] = None,
    contract_amount_max: Optional[float] = None
) -> List[Construction]:
    """
    필터 조건에 맞는 공사 목록을 조회합니다.
    """
    filters = ConstructionFilter(
        name=name,
        construction_number=construction_number,
        type=type,
        status=status,
        location=location,
        client_id=client_id,
        contractor_id=contractor_id,
        supervisor_id=supervisor_id,
        start_date_from=start_date_from,
        start_date_to=start_date_to,
        planned_end_date_from=planned_end_date_from,
        planned_end_date_to=planned_end_date_to,
        contract_amount_min=contract_amount_min,
        contract_amount_max=contract_amount_max
    )
    constructions = crud.get_constructions(db=db, skip=skip, limit=limit, filters=filters)
    return constructions

@router.put("/{construction_id}", response_model=Construction)
def update_construction(
    *,
    db: Session = Depends(deps.get_db),
    construction_id: int,
    construction_in: ConstructionUpdate
) -> Construction:
    """
    공사 정보를 업데이트합니다.
    """
    construction = crud.get_construction(db=db, construction_id=construction_id)
    if not construction:
        raise HTTPException(status_code=404, detail="공사를 찾을 수 없습니다.")
    construction = crud.update_construction(db=db, construction_id=construction_id, construction=construction_in)
    return construction

@router.delete("/{construction_id}")
def delete_construction(
    *,
    db: Session = Depends(deps.get_db),
    construction_id: int
) -> dict:
    """
    공사를 삭제합니다.
    """
    construction = crud.get_construction(db=db, construction_id=construction_id)
    if not construction:
        raise HTTPException(status_code=404, detail="공사를 찾을 수 없습니다.")
    crud.delete_construction(db=db, construction_id=construction_id)
    return {"message": "공사가 삭제되었습니다."}

@router.get("/status/{status}", response_model=List[Construction])
def get_constructions_by_status(
    *,
    db: Session = Depends(deps.get_db),
    status: ConstructionStatus,
    skip: int = 0,
    limit: int = 100
) -> List[Construction]:
    """
    상태별 공사 목록을 조회합니다.
    """
    constructions = crud.get_constructions_by_status(db=db, status=status, skip=skip, limit=limit)
    return constructions

@router.get("/type/{type}", response_model=List[Construction])
def get_constructions_by_type(
    *,
    db: Session = Depends(deps.get_db),
    type: ConstructionType,
    skip: int = 0,
    limit: int = 100
) -> List[Construction]:
    """
    유형별 공사 목록을 조회합니다.
    """
    constructions = crud.get_constructions_by_type(db=db, type=type, skip=skip, limit=limit)
    return constructions

@router.get("/client/{client_id}", response_model=List[Construction])
def get_constructions_by_client(
    *,
    db: Session = Depends(deps.get_db),
    client_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Construction]:
    """
    발주자별 공사 목록을 조회합니다.
    """
    constructions = crud.get_constructions_by_client(db=db, client_id=client_id, skip=skip, limit=limit)
    return constructions

@router.get("/contractor/{contractor_id}", response_model=List[Construction])
def get_constructions_by_contractor(
    *,
    db: Session = Depends(deps.get_db),
    contractor_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Construction]:
    """
    수급자별 공사 목록을 조회합니다.
    """
    constructions = crud.get_constructions_by_contractor(db=db, contractor_id=contractor_id, skip=skip, limit=limit)
    return constructions

@router.get("/supervisor/{supervisor_id}", response_model=List[Construction])
def get_constructions_by_supervisor(
    *,
    db: Session = Depends(deps.get_db),
    supervisor_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Construction]:
    """
    감리자별 공사 목록을 조회합니다.
    """
    constructions = crud.get_constructions_by_supervisor(db=db, supervisor_id=supervisor_id, skip=skip, limit=limit)
    return constructions 