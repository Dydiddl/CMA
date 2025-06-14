"""
데이터베이스 모델 정의
이 파일은 SQLAlchemy ORM을 사용하여 데이터베이스 테이블 구조를 정의합니다.
각 클래스는 데이터베이스의 테이블을 나타내며, 클래스의 속성은 테이블의 컬럼을 정의합니다.
"""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base

class User(Base):
    """
    사용자 정보를 저장하는 테이블
    사용자의 기본 정보와 인증 정보를 관리합니다.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # 사용자 고유 식별자
    email = Column(String, unique=True, index=True)  # 이메일 주소 (고유)
    username = Column(String, unique=True, index=True)  # 사용자 이름 (고유)
    hashed_password = Column(String)  # 암호화된 비밀번호
    is_active = Column(Boolean, default=True)  # 계정 활성화 상태
    role = Column(String, default="USER")  # 사용자 역할 (USER, ADMIN 등)
    created_at = Column(DateTime, default=datetime.utcnow)  # 계정 생성 일시
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 정보 수정 일시

    # 관계 설정: 사용자가 소유한 프로젝트 목록
    projects = relationship("Project", back_populates="owner")

class Project(Base):
    """
    프로젝트 정보를 저장하는 테이블
    건설 프로젝트의 기본 정보와 진행 상태를 관리합니다.
    """
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)  # 프로젝트 고유 식별자
    name = Column(String, index=True)  # 프로젝트명
    description = Column(String)  # 프로젝트 설명
    status = Column(String)  # 프로젝트 상태 (진행중, 완료, 중단 등)
    start_date = Column(DateTime)  # 프로젝트 시작일
    end_date = Column(DateTime)  # 프로젝트 종료일
    owner_id = Column(Integer, ForeignKey("users.id"))  # 프로젝트 소유자 ID
    created_at = Column(DateTime, default=datetime.utcnow)  # 프로젝트 생성 일시
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 정보 수정 일시

    # 관계 설정
    owner = relationship("User", back_populates="projects")  # 프로젝트 소유자
    tasks = relationship("Task", back_populates="project")  # 프로젝트의 태스크 목록

class Task(Base):
    """
    태스크 정보를 저장하는 테이블
    프로젝트 내의 개별 작업 항목을 관리합니다.
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)  # 태스크 고유 식별자
    name = Column(String, index=True)  # 태스크명
    description = Column(String)  # 태스크 설명
    status = Column(String)  # 태스크 상태 (대기중, 진행중, 완료 등)
    progress = Column(Float, default=0.0)  # 진행률 (0.0 ~ 1.0)
    start_date = Column(DateTime)  # 태스크 시작일
    end_date = Column(DateTime)  # 태스크 종료일
    project_id = Column(Integer, ForeignKey("projects.id"))  # 소속 프로젝트 ID
    created_at = Column(DateTime, default=datetime.utcnow)  # 태스크 생성 일시
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 정보 수정 일시

    # 관계 설정: 태스크가 속한 프로젝트
    project = relationship("Project", back_populates="tasks") 