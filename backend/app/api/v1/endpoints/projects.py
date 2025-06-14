from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.core.permissions import check_permissions
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate, Project
from app.crud import project as project_crud

router = APIRouter()

@router.post("/", response_model=Project)
def create_project(
    *,
    db: Session = Depends(deps.get_db),
    project_in: ProjectCreate,
    current_user: User = Depends(deps.get_current_user)
) -> Project:
    """
    새로운 프로젝트를 생성합니다.
    """
    if not check_permissions(current_user, ["create:project"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="프로젝트 생성 권한이 없습니다"
        )
    
    project = project_crud.create(db=db, obj_in=project_in, owner_id=current_user.id)
    return project

@router.get("/", response_model=List[Project])
def read_projects(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> List[Project]:
    """
    프로젝트 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:project"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="프로젝트 조회 권한이 없습니다"
        )
    
    projects = project_crud.get_multi(db, skip=skip, limit=limit)
    return projects

@router.get("/{project_id}", response_model=Project)
def read_project(
    *,
    db: Session = Depends(deps.get_db),
    project_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> Project:
    """
    특정 프로젝트를 조회합니다.
    """
    if not check_permissions(current_user, ["read:project"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="프로젝트 조회 권한이 없습니다"
        )
    
    project = project_crud.get(db=db, id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="프로젝트를 찾을 수 없습니다"
        )
    return project

@router.put("/{project_id}", response_model=Project)
def update_project(
    *,
    db: Session = Depends(deps.get_db),
    project_id: int,
    project_in: ProjectUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> Project:
    """
    프로젝트 정보를 업데이트합니다.
    """
    if not check_permissions(current_user, ["update:project"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="프로젝트 수정 권한이 없습니다"
        )
    
    project = project_crud.get(db=db, id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="프로젝트를 찾을 수 없습니다"
        )
    
    project = project_crud.update(db=db, db_obj=project, obj_in=project_in)
    return project

@router.delete("/{project_id}")
def delete_project(
    *,
    db: Session = Depends(deps.get_db),
    project_id: int,
    current_user: User = Depends(deps.get_current_user)
):
    """
    프로젝트를 삭제합니다.
    """
    if not check_permissions(current_user, ["delete:project"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="프로젝트 삭제 권한이 없습니다"
        )
    
    project = project_crud.get(db=db, id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="프로젝트를 찾을 수 없습니다"
        )
    
    project_crud.remove(db=db, id=project_id)
    return {"status": "success"} 