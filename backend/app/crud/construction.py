from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime

from app.models.construction import Construction
from app.schemas.construction import ConstructionCreate, ConstructionUpdate, ConstructionFilter

def create_construction(db: Session, construction: ConstructionCreate) -> Construction:
    """
    새로운 공사를 생성합니다.
    """
    db_construction = Construction(**construction.dict())
    db.add(db_construction)
    db.commit()
    db.refresh(db_construction)
    return db_construction

def get_construction(db: Session, construction_id: int) -> Optional[Construction]:
    """
    ID로 공사를 조회합니다.
    """
    return db.query(Construction).filter(Construction.id == construction_id).first()

def get_construction_by_number(db: Session, construction_number: str) -> Optional[Construction]:
    """
    공사번호로 공사를 조회합니다.
    """
    return db.query(Construction).filter(Construction.construction_number == construction_number).first()

def get_constructions(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    filters: Optional[ConstructionFilter] = None
) -> List[Construction]:
    """
    필터 조건에 맞는 공사 목록을 조회합니다.
    """
    query = db.query(Construction)
    
    if filters:
        conditions = []
        
        if filters.name:
            conditions.append(Construction.name.ilike(f"%{filters.name}%"))
        if filters.construction_number:
            conditions.append(Construction.construction_number.ilike(f"%{filters.construction_number}%"))
        if filters.type:
            conditions.append(Construction.type == filters.type)
        if filters.status:
            conditions.append(Construction.status == filters.status)
        if filters.location:
            conditions.append(Construction.location.ilike(f"%{filters.location}%"))
        if filters.client_id:
            conditions.append(Construction.client_id == filters.client_id)
        if filters.contractor_id:
            conditions.append(Construction.contractor_id == filters.contractor_id)
        if filters.supervisor_id:
            conditions.append(Construction.supervisor_id == filters.supervisor_id)
        if filters.start_date_from:
            conditions.append(Construction.start_date >= filters.start_date_from)
        if filters.start_date_to:
            conditions.append(Construction.start_date <= filters.start_date_to)
        if filters.planned_end_date_from:
            conditions.append(Construction.planned_end_date >= filters.planned_end_date_from)
        if filters.planned_end_date_to:
            conditions.append(Construction.planned_end_date <= filters.planned_end_date_to)
        if filters.contract_amount_min:
            conditions.append(Construction.contract_amount >= filters.contract_amount_min)
        if filters.contract_amount_max:
            conditions.append(Construction.contract_amount <= filters.contract_amount_max)
            
        if conditions:
            query = query.filter(and_(*conditions))
    
    return query.offset(skip).limit(limit).all()

def update_construction(
    db: Session,
    construction_id: int,
    construction: ConstructionUpdate
) -> Optional[Construction]:
    """
    공사 정보를 업데이트합니다.
    """
    db_construction = get_construction(db, construction_id)
    if not db_construction:
        return None
        
    update_data = construction.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_construction, field, value)
    
    db_construction.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_construction)
    return db_construction

def delete_construction(db: Session, construction_id: int) -> bool:
    """
    공사를 삭제합니다.
    """
    db_construction = get_construction(db, construction_id)
    if not db_construction:
        return False
        
    db.delete(db_construction)
    db.commit()
    return True

def get_constructions_by_status(
    db: Session,
    status: str,
    skip: int = 0,
    limit: int = 100
) -> List[Construction]:
    """
    상태별 공사 목록을 조회합니다.
    """
    return db.query(Construction)\
        .filter(Construction.status == status)\
        .offset(skip)\
        .limit(limit)\
        .all()

def get_constructions_by_type(
    db: Session,
    type: str,
    skip: int = 0,
    limit: int = 100
) -> List[Construction]:
    """
    유형별 공사 목록을 조회합니다.
    """
    return db.query(Construction)\
        .filter(Construction.type == type)\
        .offset(skip)\
        .limit(limit)\
        .all()

def get_constructions_by_client(
    db: Session,
    client_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Construction]:
    """
    발주자별 공사 목록을 조회합니다.
    """
    return db.query(Construction)\
        .filter(Construction.client_id == client_id)\
        .offset(skip)\
        .limit(limit)\
        .all()

def get_constructions_by_contractor(
    db: Session,
    contractor_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Construction]:
    """
    수급자별 공사 목록을 조회합니다.
    """
    return db.query(Construction)\
        .filter(Construction.contractor_id == contractor_id)\
        .offset(skip)\
        .limit(limit)\
        .all()

def get_constructions_by_supervisor(
    db: Session,
    supervisor_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Construction]:
    """
    감리자별 공사 목록을 조회합니다.
    """
    return db.query(Construction)\
        .filter(Construction.supervisor_id == supervisor_id)\
        .offset(skip)\
        .limit(limit)\
        .all() 