from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate

class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: ProjectCreate, owner_id: int
    ) -> Project:
        """
        소유자 정보와 함께 프로젝트 생성
        """
        obj_in_data = obj_in.dict()
        obj_in_data["owner_id"] = owner_id
        return super().create(db, obj_in=obj_in_data)

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        """
        소유자별 프로젝트 목록 조회
        """
        return (
            db.query(self.model)
            .filter(Project.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_name(
        self, db: Session, *, name: str, owner_id: int
    ) -> Optional[Project]:
        """
        프로젝트 이름으로 조회
        """
        return (
            db.query(self.model)
            .filter(Project.name == name, Project.owner_id == owner_id)
            .first()
        )

    def get_active_projects(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        """
        활성화된 프로젝트 목록 조회
        """
        return (
            db.query(self.model)
            .filter(Project.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_projects_by_status(
        self, db: Session, *, status: str, skip: int = 0, limit: int = 100
    ) -> List[Project]:
        """
        상태별 프로젝트 목록 조회
        """
        return (
            db.query(self.model)
            .filter(Project.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

project = CRUDProject(Project) 