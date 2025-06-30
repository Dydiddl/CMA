from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.schemas import Task, TaskCreate, TaskUpdate
from app.models.models import User
from app.crud import get_tasks, create_task, get_task, update_task, delete_task
from app.core.auth import get_current_user
from app.db.database import get_db

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.get("/", response_model=List[Task])
def get_tasks_route(project_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_tasks(db, project_id=project_id, skip=skip, limit=limit)

@router.post("/", response_model=Task)
def create_task_route(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_task(db=db, task=task)

@router.get("/{task_id}", response_model=Task)
def get_task_route(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=Task)
def update_task_route(task_id: int, task: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_task = update_task(db, task_id=task_id, task=task)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/{task_id}")
def delete_task_route(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success = delete_task(db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}
