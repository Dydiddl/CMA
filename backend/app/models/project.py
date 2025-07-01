#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
프로젝트 모델 - 건설 프로젝트 관리
"""

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float, Text, Boolean, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..db.database import Base
import uuid

class ProjectStatus(str, enum.Enum):
    """프로젝트 상태 열거형"""
    PLANNING = "planning"  # 기획
    PREPARATION = "preparation"  # 준비
    IN_PROGRESS = "in_progress"  # 진행중
    COMPLETED = "completed"  # 완료
    ON_HOLD = "on_hold"  # 일시중단
    CANCELLED = "cancelled"  # 취소

class ProjectType(str, enum.Enum):
    """프로젝트 유형 열거형"""
    RESIDENTIAL = "residential"  # 주거
    COMMERCIAL = "commercial"  # 상업
    INFRASTRUCTURE = "infrastructure"  # 인프라
    INDUSTRIAL = "industrial"  # 산업
    MIXED_USE = "mixed_use"  # 복합용도
    OTHER = "other"  # 기타

class Project(Base):
    """프로젝트 모델"""
    __tablename__ = "projects"
    
    # 기본 정보
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, index=True, comment="프로젝트명")
    project_number = Column(String(50), unique=True, nullable=False, index=True, comment="프로젝트 번호")
    description = Column(Text, nullable=True, comment="프로젝트 설명")
    
    # 프로젝트 유형 및 상태
    project_type = Column(Enum(ProjectType), nullable=False, default=ProjectType.OTHER, comment="프로젝트 유형")
    status = Column(Enum(ProjectStatus), nullable=False, default=ProjectStatus.PLANNING, comment="프로젝트 상태")
    
    # 위치 정보
    location = Column(String(500), nullable=True, comment="프로젝트 위치")
    address = Column(String(500), nullable=True, comment="상세 주소")
    
    # 일정 정보
    start_date = Column(DateTime, nullable=True, comment="시작일")
    end_date = Column(DateTime, nullable=True, comment="종료일")
    planned_start_date = Column(DateTime, nullable=True, comment="계획 시작일")
    planned_end_date = Column(DateTime, nullable=True, comment="계획 종료일")
    
    # 예산 정보
    total_budget = Column(Float, nullable=True, comment="총 예산")
    current_cost = Column(Float, nullable=True, default=0.0, comment="현재 비용")
    remaining_budget = Column(Float, nullable=True, comment="잔여 예산")
    
    # 관리 정보
    project_manager = Column(String(100), nullable=True, comment="프로젝트 매니저")
    client_name = Column(String(255), nullable=True, comment="발주처명")
    client_contact = Column(String(100), nullable=True, comment="발주처 연락처")
    
    # 기술 정보
    building_area = Column(Float, nullable=True, comment="건축면적 (㎡)")
    floor_area = Column(Float, nullable=True, comment="연면적 (㎡)")
    floors = Column(Integer, nullable=True, comment="층수")
    
    # 외래키
    vendor_id = Column(String, ForeignKey("vendors.id"), nullable=True, comment="거래처 ID")
    
    # 관계 설정
    vendor = relationship("Vendor", back_populates="projects")
    contracts = relationship("Contract", back_populates="project", cascade="all, delete-orphan")
    financial_records = relationship("FinancialRecord", back_populates="project", cascade="all, delete-orphan")
    labors = relationship("Labor", back_populates="project", cascade="all, delete-orphan")
    documents = relationship("ProjectDocument", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}', project_number='{self.project_number}')>"
    
    def calculate_progress(self) -> float:
        """프로젝트 진행률 계산"""
        if not self.start_date or not self.end_date:
            return 0.0
        
        total_days = (self.end_date - self.start_date).days
        if total_days <= 0:
            return 100.0 if self.status == ProjectStatus.COMPLETED else 0.0
        
        current_date = datetime.now()
        if current_date < self.start_date:
            return 0.0
        elif current_date > self.end_date:
            return 100.0
        
        elapsed_days = (current_date - self.start_date).days
        return min(100.0, (elapsed_days / total_days) * 100)
    
    def calculate_budget_usage(self) -> float:
        """예산 사용률 계산"""
        if not self.total_budget or self.total_budget <= 0:
            return 0.0
        
        current_cost = self.current_cost or 0.0
        return min(100.0, (current_cost / self.total_budget) * 100)
    
    def update_budget_info(self):
        """예산 정보 업데이트"""
        if self.total_budget and self.current_cost:
            self.remaining_budget = self.total_budget - self.current_cost

class ProjectDocument(Base):
    """프로젝트 문서 모델"""
    __tablename__ = "project_documents"
    
    # 기본 정보
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False, comment="문서 제목")
    file_name = Column(String(255), nullable=False, comment="파일명")
    file_path = Column(String(500), nullable=False, comment="파일 경로")
    file_size = Column(Integer, nullable=True, comment="파일 크기 (bytes)")
    file_type = Column(String(50), nullable=True, comment="파일 유형")
    
    # 문서 분류
    document_type = Column(String(100), nullable=True, comment="문서 유형")
    category = Column(String(100), nullable=True, comment="문서 카테고리")
    
    # 메타데이터
    description = Column(Text, nullable=True, comment="문서 설명")
    tags = Column(String(500), nullable=True, comment="태그 (쉼표로 구분)")
    version = Column(String(20), nullable=True, default="1.0", comment="문서 버전")
    
    # 외래키
    project_id = Column(String, ForeignKey("projects.id"), nullable=False, comment="프로젝트 ID")
    
    # 관계 설정
    project = relationship("Project", back_populates="documents")
    
    def __repr__(self):
        return f"<ProjectDocument(id={self.id}, title='{self.title}', project_id='{self.project_id}')>" 