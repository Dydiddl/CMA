#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
프로젝트 서비스 - 비즈니스 로직
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime
import logging

from app.models.project import Project, ProjectDocument, ProjectStatus, ProjectType
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectDocumentCreate, ProjectDocumentUpdate
from app.core.exceptions import NotFoundException, ValidationException

logger = logging.getLogger(__name__)

class ProjectService:
    """프로젝트 서비스 클래스"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_project(self, project_data: ProjectCreate) -> Project:
        """프로젝트 생성"""
        # 프로젝트 번호 중복 검사
        existing_project = self.db.query(Project).filter(
            Project.project_number == project_data.project_number
        ).first()
        
        if existing_project:
            raise ValidationException("이미 존재하는 프로젝트 번호입니다.")
        
        # 프로젝트 생성
        project = Project(**project_data.dict())
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        
        logger.info(f"프로젝트 생성 완료: {project.project_number}")
        return project
    
    def get_projects(
        self, 
        skip: int = 0, 
        limit: int = 10, 
        search: Optional[str] = None,
        status: Optional[ProjectStatus] = None,
        project_type: Optional[ProjectType] = None
    ) -> Tuple[List[Project], int]:
        """프로젝트 목록 조회"""
        query = self.db.query(Project)
        
        # 검색 조건 적용
        if search:
            query = query.filter(
                or_(
                    Project.name.contains(search),
                    Project.project_number.contains(search),
                    Project.client_name.contains(search),
                    Project.project_manager.contains(search)
                )
            )
        
        # 상태 필터 적용
        if status:
            query = query.filter(Project.status == status)
        
        # 프로젝트 유형 필터 적용
        if project_type:
            query = query.filter(Project.project_type == project_type)
        
        # 전체 개수 조회
        total = query.count()
        
        # 페이징 적용
        projects = query.offset(skip).limit(limit).all()
        
        return projects, total
    
    def get_project_by_id(self, project_id: str) -> Optional[Project]:
        """프로젝트 ID로 조회"""
        project = self.db.query(Project).filter(Project.id == project_id).first()
        return project
    
    def update_project(
        self, 
        project_id: str, 
        project_update: ProjectUpdate
    ) -> Optional[Project]:
        """프로젝트 수정"""
        project = self.db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return None
        
        # 업데이트할 데이터만 추출
        update_data = project_update.dict(exclude_unset=True)
        
        # 프로젝트 번호 변경 시 중복 검사
        if 'project_number' in update_data:
            existing_project = self.db.query(Project).filter(
                and_(
                    Project.project_number == update_data['project_number'],
                    Project.id != project_id
                )
            ).first()
            if existing_project:
                raise ValidationException("이미 존재하는 프로젝트 번호입니다.")
        
        # 프로젝트 정보 업데이트
        for field, value in update_data.items():
            setattr(project, field, value)
        
        # 예산 정보 업데이트
        project.update_budget_info()
        
        self.db.commit()
        self.db.refresh(project)
        
        logger.info(f"프로젝트 수정 완료: {project.project_number}")
        return project
    
    def delete_project(self, project_id: str) -> bool:
        """프로젝트 삭제"""
        project = self.db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return False
        
        self.db.delete(project)
        self.db.commit()
        
        logger.info(f"프로젝트 삭제 완료: {project.project_number}")
        return True
    
    def get_project_statistics(self) -> Dict[str, Any]:
        """프로젝트 통계 조회"""
        # 전체 프로젝트 수
        total_projects = self.db.query(Project).count()
        
        # 활성 프로젝트 수 (진행중, 준비)
        active_projects = self.db.query(Project).filter(
            Project.status.in_([ProjectStatus.IN_PROGRESS, ProjectStatus.PREPARATION])
        ).count()
        
        # 완료된 프로젝트 수
        completed_projects = self.db.query(Project).filter(
            Project.status == ProjectStatus.COMPLETED
        ).count()
        
        # 총 예산 및 지출
        budget_stats = self.db.query(
            func.sum(Project.total_budget).label('total_budget'),
            func.sum(Project.current_cost).label('total_spent')
        ).first()
        
        total_budget = float(budget_stats.total_budget or 0)
        total_spent = float(budget_stats.total_spent or 0)
        
        # 평균 진행률
        projects_with_dates = self.db.query(Project).filter(
            and_(Project.start_date.isnot(None), Project.end_date.isnot(None))
        ).all()
        
        if projects_with_dates:
            total_progress = sum(project.calculate_progress() for project in projects_with_dates)
            average_progress = total_progress / len(projects_with_dates)
        else:
            average_progress = 0.0
        
        # 상태별 프로젝트 수
        projects_by_status = {}
        for status in ProjectStatus:
            count = self.db.query(Project).filter(Project.status == status).count()
            projects_by_status[status.value] = count
        
        # 유형별 프로젝트 수
        projects_by_type = {}
        for project_type in ProjectType:
            count = self.db.query(Project).filter(Project.project_type == project_type).count()
            projects_by_type[project_type.value] = count
        
        return {
            "total_projects": total_projects,
            "active_projects": active_projects,
            "completed_projects": completed_projects,
            "total_budget": total_budget,
            "total_spent": total_spent,
            "average_progress": average_progress,
            "projects_by_status": projects_by_status,
            "projects_by_type": projects_by_type
        }
    
    def create_project_document(self, document_data: ProjectDocumentCreate) -> ProjectDocument:
        """프로젝트 문서 생성"""
        # 프로젝트 존재 확인
        project = self.db.query(Project).filter(Project.id == document_data.project_id).first()
        if not project:
            raise NotFoundException("프로젝트를 찾을 수 없습니다.")
        
        # 문서 생성
        document = ProjectDocument(**document_data.dict())
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        
        logger.info(f"프로젝트 문서 생성 완료: {document.title}")
        return document
    
    def get_project_documents(
        self, 
        project_id: str,
        skip: int = 0, 
        limit: int = 10
    ) -> Tuple[List[ProjectDocument], int]:
        """프로젝트 문서 목록 조회"""
        query = self.db.query(ProjectDocument).filter(
            ProjectDocument.project_id == project_id
        )
        
        # 전체 개수 조회
        total = query.count()
        
        # 페이징 적용
        documents = query.offset(skip).limit(limit).all()
        
        return documents, total
    
    def get_project_document_by_id(self, document_id: str) -> Optional[ProjectDocument]:
        """프로젝트 문서 ID로 조회"""
        document = self.db.query(ProjectDocument).filter(
            ProjectDocument.id == document_id
        ).first()
        return document
    
    def update_project_document(
        self, 
        document_id: str, 
        document_update: ProjectDocumentUpdate
    ) -> Optional[ProjectDocument]:
        """프로젝트 문서 수정"""
        document = self.db.query(ProjectDocument).filter(
            ProjectDocument.id == document_id
        ).first()
        if not document:
            return None
        
        # 업데이트할 데이터만 추출
        update_data = document_update.dict(exclude_unset=True)
        
        # 문서 정보 업데이트
        for field, value in update_data.items():
            setattr(document, field, value)
        
        self.db.commit()
        self.db.refresh(document)
        
        logger.info(f"프로젝트 문서 수정 완료: {document.title}")
        return document
    
    def delete_project_document(self, document_id: str) -> bool:
        """프로젝트 문서 삭제"""
        document = self.db.query(ProjectDocument).filter(
            ProjectDocument.id == document_id
        ).first()
        if not document:
            return False
        
        self.db.delete(document)
        self.db.commit()
        
        logger.info(f"프로젝트 문서 삭제 완료: {document.title}")
        return True
    
    def get_projects_by_vendor(self, vendor_id: str) -> List[Project]:
        """거래처별 프로젝트 조회"""
        projects = self.db.query(Project).filter(
            Project.vendor_id == vendor_id
        ).all()
        return projects
    
    def get_projects_by_date_range(
        self, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[Project]:
        """기간별 프로젝트 조회"""
        projects = self.db.query(Project).filter(
            and_(
                Project.start_date >= start_date,
                Project.end_date <= end_date
            )
        ).all()
        return projects 