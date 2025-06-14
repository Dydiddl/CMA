from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Float, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base_class import Base

class ProgressStatus(str, enum.Enum):
    ON_SCHEDULE = "on_schedule"  # 예정대로
    DELAYED = "delayed"  # 지연
    AHEAD = "ahead"  # 진행
    COMPLETED = "completed"  # 완료
    SUSPENDED = "suspended"  # 중단

class ConstructionProgress(Base):
    __tablename__ = "construction_progress"

    id = Column(Integer, primary_key=True, index=True)
    construction_id = Column(Integer, ForeignKey("constructions.id"), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # 공정 정보
    progress_percentage = Column(Float, nullable=False)  # 공정률
    status = Column(Enum(ProgressStatus), default=ProgressStatus.ON_SCHEDULE)
    description = Column(Text, nullable=True)  # 작업 내용
    
    # 작업 정보
    work_type = Column(String(100), nullable=False)  # 작업 종류
    work_area = Column(String(200), nullable=True)  # 작업 구역
    worker_count = Column(Integer, nullable=True)  # 작업자 수
    equipment_count = Column(Integer, nullable=True)  # 장비 수
    
    # 날씨 정보
    weather = Column(String(50), nullable=True)  # 날씨
    temperature = Column(Float, nullable=True)  # 기온
    humidity = Column(Float, nullable=True)  # 습도
    
    # 특이사항
    issues = Column(Text, nullable=True)  # 특이사항
    solutions = Column(Text, nullable=True)  # 해결방안
    
    # 관계 설정
    construction = relationship("Construction", back_populates="progress")
    photos = relationship("ConstructionPhoto", back_populates="progress")
    safety_checks = relationship("SafetyCheck", back_populates="progress")
    quality_checks = relationship("QualityCheck", back_populates="progress")
    
    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class ConstructionPhoto(Base):
    __tablename__ = "construction_photos"

    id = Column(Integer, primary_key=True, index=True)
    progress_id = Column(Integer, ForeignKey("construction_progress.id"), nullable=False)
    photo_url = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    taken_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # 관계 설정
    progress = relationship("ConstructionProgress", back_populates="photos")
    
    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class SafetyCheck(Base):
    __tablename__ = "safety_checks"

    id = Column(Integer, primary_key=True, index=True)
    progress_id = Column(Integer, ForeignKey("construction_progress.id"), nullable=False)
    check_type = Column(String(100), nullable=False)  # 점검 종류
    check_result = Column(String(50), nullable=False)  # 점검 결과
    issues = Column(Text, nullable=True)  # 발견된 문제점
    actions = Column(Text, nullable=True)  # 조치사항
    checker = Column(String(100), nullable=False)  # 점검자
    
    # 관계 설정
    progress = relationship("ConstructionProgress", back_populates="safety_checks")
    
    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class QualityCheck(Base):
    __tablename__ = "quality_checks"

    id = Column(Integer, primary_key=True, index=True)
    progress_id = Column(Integer, ForeignKey("construction_progress.id"), nullable=False)
    check_type = Column(String(100), nullable=False)  # 점검 종류
    check_result = Column(String(50), nullable=False)  # 점검 결과
    issues = Column(Text, nullable=True)  # 발견된 문제점
    actions = Column(Text, nullable=True)  # 조치사항
    checker = Column(String(100), nullable=False)  # 점검자
    
    # 관계 설정
    progress = relationship("ConstructionProgress", back_populates="quality_checks")
    
    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False) 