from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, timedelta
from app.crud.base import CRUDBase
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate

class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    def create_with_creator(
        self, db: Session, *, obj_in: TaskCreate, creator_id: int
    ) -> Task:
        """
        생성자 정보와 함께 작업 생성
        """
        obj_in_data = obj_in.dict()
        obj_in_data["creator_id"] = creator_id
        return super().create(db, obj_in=obj_in_data)

    def get_multi_by_project(
        self, db: Session, *, project_id: int, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        """
        프로젝트별 작업 목록 조회
        """
        return (
            db.query(self.model)
            .filter(Task.project_id == project_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_assignee(
        self, db: Session, *, assignee_id: int, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        """
        담당자별 작업 목록 조회
        """
        return (
            db.query(self.model)
            .filter(Task.assignee_id == assignee_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_status(
        self, db: Session, *, status: TaskStatus, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        """
        상태별 작업 목록 조회
        """
        return (
            db.query(self.model)
            .filter(Task.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_completed(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        """
        완료된 작업 목록 조회
        """
        return (
            db.query(self.model)
            .filter(Task.is_completed == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_due_soon(
        self, db: Session, *, days: int = 7, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        """
        마감이 임박한 작업 목록 조회
        """
        due_date = datetime.utcnow() + timedelta(days=days)
        return (
            db.query(self.model)
            .filter(
                Task.due_date <= due_date,
                Task.is_completed == False
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_overdue_tasks(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        """
        마감일이 지난 작업 목록 조회
        """
        return (
            db.query(self.model)
            .filter(
                and_(
                    Task.due_date < datetime.utcnow(),
                    Task.is_completed == False
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_tasks_due_today(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        """
        오늘 마감인 작업 목록 조회
        """
        today = datetime.utcnow().date()
        tomorrow = today + timedelta(days=1)
        
        return (
            db.query(self.model)
            .filter(
                and_(
                    Task.due_date >= today,
                    Task.due_date < tomorrow,
                    Task.is_completed == False
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_tasks_due_this_week(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        """
        이번 주 마감인 작업 목록 조회
        """
        today = datetime.utcnow().date()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=7)
        
        return (
            db.query(self.model)
            .filter(
                and_(
                    Task.due_date >= week_start,
                    Task.due_date < week_end,
                    Task.is_completed == False
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_tasks_due_this_month(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        """
        이번 달 마감인 작업 목록 조회
        """
        today = datetime.utcnow().date()
        month_start = today.replace(day=1)
        if today.month == 12:
            month_end = today.replace(year=today.year + 1, month=1, day=1)
        else:
            month_end = today.replace(month=today.month + 1, day=1)
        
        return (
            db.query(self.model)
            .filter(
                and_(
                    Task.due_date >= month_start,
                    Task.due_date < month_end,
                    Task.is_completed == False
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_due_date(
        self, db: Session, *, task_id: int, new_due_date: datetime
    ) -> Optional[Task]:
        """
        작업 마감일 수정
        """
        task = self.get(db=db, id=task_id)
        if not task:
            return None
        
        task.due_date = new_due_date
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    def extend_due_date(
        self, db: Session, *, task_id: int, days: int
    ) -> Optional[Task]:
        """
        작업 마감일 연장
        """
        task = self.get(db=db, id=task_id)
        if not task or not task.due_date:
            return None
        
        new_due_date = task.due_date + timedelta(days=days)
        return self.update_due_date(db=db, task_id=task_id, new_due_date=new_due_date)

task = CRUDTask(Task) 