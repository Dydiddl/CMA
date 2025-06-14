from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.core.permissions import check_permissions
from app.models.user import User
from app.schemas.department import DepartmentCreate, DepartmentUpdate, Department
from app.crud import department as department_crud

router = APIRouter()

@router.post("/", response_model=Department)
def create_department(
    *,
    db: Session = Depends(deps.get_db),
    department_in: DepartmentCreate,
    current_user: User = Depends(deps.get_current_user)
) -> Department:
    """
    새로운 부서를 생성합니다.
    """
    if not check_permissions(current_user, ["manage:departments"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="부서 생성 권한이 없습니다"
        )
    
    department = department_crud.create(db=db, obj_in=department_in)
    return department

@router.get("/", response_model=List[Department])
def read_departments(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> List[Department]:
    """
    부서 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["manage:departments"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="부서 조회 권한이 없습니다"
        )
    
    departments = department_crud.get_multi(db, skip=skip, limit=limit)
    return departments

@router.get("/{department_id}", response_model=Department)
def read_department(
    *,
    db: Session = Depends(deps.get_db),
    department_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> Department:
    """
    특정 부서를 조회합니다.
    """
    if not check_permissions(current_user, ["manage:departments"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="부서 조회 권한이 없습니다"
        )
    
    department = department_crud.get(db=db, id=department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="부서를 찾을 수 없습니다"
        )
    return department

@router.put("/{department_id}", response_model=Department)
def update_department(
    *,
    db: Session = Depends(deps.get_db),
    department_id: int,
    department_in: DepartmentUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> Department:
    """
    부서를 수정합니다.
    """
    if not check_permissions(current_user, ["manage:departments"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="부서 수정 권한이 없습니다"
        )
    
    department = department_crud.get(db=db, id=department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="부서를 찾을 수 없습니다"
        )
    
    department = department_crud.update(db=db, db_obj=department, obj_in=department_in)
    return department

@router.delete("/{department_id}", response_model=Department)
def delete_department(
    *,
    db: Session = Depends(deps.get_db),
    department_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> Department:
    """
    부서를 삭제합니다.
    """
    if not check_permissions(current_user, ["manage:departments"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="부서 삭제 권한이 없습니다"
        )
    
    department = department_crud.get(db=db, id=department_id)
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="부서를 찾을 수 없습니다"
        )
    
    department = department_crud.remove(db=db, id=department_id)
    return department 