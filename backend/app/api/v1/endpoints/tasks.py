from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.api import deps
from app.core.permissions import check_permissions
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, Task
from app.crud import task as task_crud

router = APIRouter()

@router.post("/", response_model=Task)
def create_task(
    *,
    db: Session = Depends(deps.get_db),
    task_in: TaskCreate,
    current_user: User = Depends(deps.get_current_user)
) -> Task:
    """
    새로운 작업을 생성합니다.
    """
    if not check_permissions(current_user, ["create:task"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="작업 생성 권한이 없습니다"
        )
    
    task = task_crud.create(db=db, obj_in=task_in, creator_id=current_user.id)
    return task

@router.get("/", response_model=List[Task])
def read_tasks(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[int] = None,
    assignee_id: Optional[int] = None,
    current_user: User = Depends(deps.get_current_user)
) -> List[Task]:
    """
    작업 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:task"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="작업 조회 권한이 없습니다"
        )
    
    tasks = task_crud.get_multi(
        db=db,
        skip=skip,
        limit=limit,
        project_id=project_id,
        assignee_id=assignee_id
    )
    return tasks

@router.get("/{task_id}", response_model=Task)
def read_task(
    *,
    db: Session = Depends(deps.get_db),
    task_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> Task:
    """
    특정 작업을 조회합니다.
    """
    if not check_permissions(current_user, ["read:task"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="작업 조회 권한이 없습니다"
        )
    
    task = task_crud.get(db=db, id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="작업을 찾을 수 없습니다"
        )
    return task

@router.put("/{task_id}", response_model=Task)
def update_task(
    *,
    db: Session = Depends(deps.get_db),
    task_id: int,
    task_in: TaskUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> Task:
    """
    작업 정보를 업데이트합니다.
    """
    if not check_permissions(current_user, ["update:task"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="작업 수정 권한이 없습니다"
        )
    
    task = task_crud.get(db=db, id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="작업을 찾을 수 없습니다"
        )
    
    task = task_crud.update(db=db, db_obj=task, obj_in=task_in)
    return task

@router.delete("/{task_id}")
def delete_task(
    *,
    db: Session = Depends(deps.get_db),
    task_id: int,
    current_user: User = Depends(deps.get_current_user)
):
    """
    작업을 삭제합니다.
    """
    if not check_permissions(current_user, ["delete:task"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="작업 삭제 권한이 없습니다"
        )
    
    task = task_crud.get(db=db, id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="작업을 찾을 수 없습니다"
        )
    
    task_crud.remove(db=db, id=task_id)
    return {"status": "success"}

@router.get("/overdue", response_model=List[Task])
def read_overdue_tasks(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> List[Task]:
    """
    마감일이 지난 작업 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:task"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="작업 조회 권한이 없습니다"
        )
    
    tasks = task_crud.get_overdue_tasks(db=db, skip=skip, limit=limit)
    return tasks

@router.get("/due-today", response_model=List[Task])
def read_tasks_due_today(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> List[Task]:
    """
    오늘 마감인 작업 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:task"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="작업 조회 권한이 없습니다"
        )
    
    tasks = task_crud.get_tasks_due_today(db=db, skip=skip, limit=limit)
    return tasks

@router.get("/due-this-week", response_model=List[Task])
def read_tasks_due_this_week(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> List[Task]:
    """
    이번 주 마감인 작업 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:task"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="작업 조회 권한이 없습니다"
        )
    
    tasks = task_crud.get_tasks_due_this_week(db=db, skip=skip, limit=limit)
    return tasks

@router.get("/due-this-month", response_model=List[Task])
def read_tasks_due_this_month(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> List[Task]:
    """
    이번 달 마감인 작업 목록을 조회합니다.
    """
    if not check_permissions(current_user, ["read:task"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="작업 조회 권한이 없습니다"
        )
    
    tasks = task_crud.get_tasks_due_this_month(db=db, skip=skip, limit=limit)
    return tasks

@router.put("/{task_id}/due-date", response_model=Task)
def update_task_due_date(
    *,
    db: Session = Depends(deps.get_db),
    task_id: int,
    new_due_date: datetime,
    current_user: User = Depends(deps.get_current_user)
) -> Task:
    """
    작업 마감일을 수정합니다.
    """
    if not check_permissions(current_user, ["update:task"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="작업 수정 권한이 없습니다"
        )
    
    task = task_crud.get(db=db, id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="작업을 찾을 수 없습니다"
        )
    
    task = task_crud.update_due_date(
        db=db,
        task_id=task_id,
        new_due_date=new_due_date
    )
    return task

@router.put("/{task_id}/extend-due-date", response_model=Task)
def extend_task_due_date(
    *,
    db: Session = Depends(deps.get_db),
    task_id: int,
    days: int,
    current_user: User = Depends(deps.get_current_user)
) -> Task:
    """
    작업 마감일을 연장합니다.
    """
    if not check_permissions(current_user, ["update:task"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="작업 수정 권한이 없습니다"
        )
    
    task = task_crud.get(db=db, id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="작업을 찾을 수 없습니다"
        )
    
    task = task_crud.extend_due_date(
        db=db,
        task_id=task_id,
        days=days
    )
    return task 