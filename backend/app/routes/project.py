from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.schemas import Project, ProjectCreate, ProjectUpdate
from app.models.models import User
from app.crud import get_projects, create_project, get_project, update_project, delete_project
from app.core.auth import get_current_user
from app.db.database import get_db

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.get("/", response_model=List[Project])
def get_projects_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_projects(db, skip=skip, limit=limit)

@router.post("/", response_model=Project)
def create_project_route(project: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_project(db=db, project=project)

@router.get("/{project_id}", response_model=Project)
def get_project_route(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = get_project(db, project_id=project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=Project)
def update_project_route(project_id: int, project: ProjectUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_project = update_project(db, project_id=project_id, project=project)
    if updated_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated_project

@router.delete("/{project_id}")
def delete_project_route(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success = delete_project(db, project_id=project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}
