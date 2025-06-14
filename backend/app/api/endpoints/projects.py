from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api import deps
from app.crud.project import project
from app.schemas.project import Project, ProjectCreate, ProjectUpdate
from app.schemas.user import User

router = APIRouter()

@router.get("/", response_model=List[Project])
def read_projects(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    프로젝트 목록 조회
    """
    if current_user.is_superuser:
        projects = project.get_multi(db, skip=skip, limit=limit)
    else:
        projects = project.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return projects

@router.post("/", response_model=Project)
def create_project(
    *,
    db: Session = Depends(deps.get_db),
    project_in: ProjectCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    새 프로젝트 생성
    """
    project_obj = project.create_with_owner(
        db=db, obj_in=project_in, owner_id=current_user.id
    )
    return project_obj

@router.get("/{project_id}", response_model=Project)
def read_project(
    *,
    db: Session = Depends(deps.get_db),
    project_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    ID로 프로젝트 조회
    """
    project_obj = project.get(db=db, id=project_id)
    if not project_obj:
        raise HTTPException(status_code=404, detail="프로젝트를 찾을 수 없습니다")
    if not current_user.is_superuser and (project_obj.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="권한이 없습니다")
    return project_obj

@router.put("/{project_id}", response_model=Project)
def update_project(
    *,
    db: Session = Depends(deps.get_db),
    project_id: int,
    project_in: ProjectUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    프로젝트 업데이트
    """
    project_obj = project.get(db=db, id=project_id)
    if not project_obj:
        raise HTTPException(status_code=404, detail="프로젝트를 찾을 수 없습니다")
    if not current_user.is_superuser and (project_obj.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="권한이 없습니다")
    project_obj = project.update(db=db, db_obj=project_obj, obj_in=project_in)
    return project_obj

@router.delete("/{project_id}", response_model=Project)
def delete_project(
    *,
    db: Session = Depends(deps.get_db),
    project_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    프로젝트 삭제
    """
    project_obj = project.get(db=db, id=project_id)
    if not project_obj:
        raise HTTPException(status_code=404, detail="프로젝트를 찾을 수 없습니다")
    if not current_user.is_superuser and (project_obj.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="권한이 없습니다")
    project_obj = project.remove(db=db, id=project_id)
    return project_obj

@router.get("/status/{status}", response_model=List[Project])
def read_projects_by_status(
    *,
    db: Session = Depends(deps.get_db),
    status: str,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    상태별 프로젝트 목록 조회
    """
    projects = project.get_projects_by_status(
        db=db, status=status, skip=skip, limit=limit
    )
    return projects

@router.get("/active/", response_model=List[Project])
def read_active_projects(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    활성화된 프로젝트 목록 조회
    """
    projects = project.get_active_projects(db=db, skip=skip, limit=limit)
    return projects 