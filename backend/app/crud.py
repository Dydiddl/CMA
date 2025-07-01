# ...existing code from crud.py...

from typing import List, Optional
from datetime import datetime
from app.schemas.schemas import Task, TaskCreate, TaskUpdate

# 임시 메모리 저장소
_fake_tasks = []
_fake_id = 1

def get_tasks(db, project_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
    return _fake_tasks[skip:skip+limit]

def create_task(db, task: TaskCreate) -> Task:
    global _fake_id
    new_task = Task(
        id=_fake_id,
        name=task.name,
        description=task.description,
        status=task.status,
        progress=task.progress,
        start_date=task.start_date or datetime.now(),
        end_date=task.end_date or datetime.now(),
        project_id=task.project_id,
        assignee=task.assignee,
        priority=task.priority,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    _fake_tasks.append(new_task)
    _fake_id += 1
    return new_task

def get_task(db, task_id: int) -> Optional[Task]:
    for t in _fake_tasks:
        if t.id == task_id:
            return t
    return None

def update_task(db, task_id: int, task: TaskUpdate) -> Optional[Task]:
    for i, t in enumerate(_fake_tasks):
        if t.id == task_id:
            updated = t.copy(update=task.dict(exclude_unset=True))
            _fake_tasks[i] = updated
            return updated
    return None

def delete_task(db, task_id: int) -> bool:
    global _fake_tasks
    for i, t in enumerate(_fake_tasks):
        if t.id == task_id:
            del _fake_tasks[i]
            return True
    return False
