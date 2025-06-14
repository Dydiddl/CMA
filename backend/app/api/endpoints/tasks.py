from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.crud.task import task
from app.schemas.task import Task, TaskCreate, TaskUpdate
from datetime import datetime

router = APIRouter()

# ... 기존 코드 ...

@router.get("/overdue", response_model=List[Task])
def read_overdue_tasks(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(deps.get_current_user),
) -> Any:
    """
    마감일이 지난 작업 목록 조회
    """
    tasks = task.get_overdue_tasks(db=db, skip=skip, limit=limit)
    return tasks

@router.get("/due-today", response_model=List[Task])
def read_tasks_due_today(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(deps.get_current_user),
) -> Any:
    """
    오늘 마감인 작업 목록 조회
    """
    tasks = task.get_tasks_due_today(db=db, skip=skip, limit=limit)
    return tasks

@router.get("/due-this-week", response_model=List[Task])
def read_tasks_due_this_week(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(deps.get_current_user),
) -> Any:
    """
    이번 주 마감인 작업 목록 조회
    """
    tasks = task.get_tasks_due_this_week(db=db, skip=skip, limit=limit)
    return tasks

@router.get("/due-this-month", response_model=List[Task])
def read_tasks_due_this_month(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(deps.get_current_user),
) -> Any:
    """
    이번 달 마감인 작업 목록 조회
    """
    tasks = task.get_tasks_due_this_month(db=db, skip=skip, limit=limit)
    return tasks

@router.put("/{task_id}/due-date", response_model=Task)
def update_task_due_date(
    *,
    db: Session = Depends(deps.get_db),
    task_id: int,
    new_due_date: datetime,
    current_user = Depends(deps.get_current_user),
) -> Any:
    """
    작업 마감일 수정
    """
    task_obj = task.get(db=db, id=task_id)
    if not task_obj:
        raise HTTPException(status_code=404, detail="작업을 찾을 수 없습니다")
    
    task_obj = task.update_due_date(
        db=db, task_id=task_id, new_due_date=new_due_date
    )
    return task_obj

@router.put("/{task_id}/extend-due-date", response_model=Task)
def extend_task_due_date(
    *,
    db: Session = Depends(deps.get_db),
    task_id: int,
    days: int,
    current_user = Depends(deps.get_current_user),
) -> Any:
    """
    작업 마감일 연장
    """
    task_obj = task.get(db=db, id=task_id)
    if not task_obj:
        raise HTTPException(status_code=404, detail="작업을 찾을 수 없습니다")
    
    task_obj = task.extend_due_date(
        db=db, task_id=task_id, days=days
    )
    return task_obj 