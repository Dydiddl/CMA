from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, JSON, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base_class import Base

class WeatherCondition(str, enum.Enum):
    SUNNY = "sunny"  # 맑음
    CLOUDY = "cloudy"  # 흐림
    RAINY = "rainy"  # 비
    SNOWY = "snowy"  # 눈
    WINDY = "windy"  # 강풍
    FOGGY = "foggy"  # 안개

class WorkStatus(str, enum.Enum):
    NORMAL = "normal"  # 정상
    DELAYED = "delayed"  # 지연
    STOPPED = "stopped"  # 중단
    COMPLETED = "completed"  # 완료

class DailyReport(Base):
    __tablename__ = "daily_reports"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    report_date = Column(DateTime, nullable=False)
    weather_condition = Column(Enum(WeatherCondition), nullable=False)
    temperature = Column(Float)  # 온도
    humidity = Column(Float)  # 습도
    work_status = Column(Enum(WorkStatus), nullable=False)
    work_description = Column(Text, nullable=False)
    work_progress = Column(Float)  # 작업 진행률
    issues = Column(Text)  # 문제점
    solutions = Column(Text)  # 해결방안
    next_day_plan = Column(Text)  # 다음날 계획
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = Column(JSON)

    # 관계 설정
    project = relationship("Project", back_populates="daily_reports")
    creator = relationship("User", back_populates="daily_reports")
    work_entries = relationship("WorkEntry", back_populates="daily_report", cascade="all, delete-orphan")
    safety_checks = relationship("SafetyCheck", back_populates="daily_report", cascade="all, delete-orphan")
    quality_checks = relationship("QualityCheck", back_populates="daily_report", cascade="all, delete-orphan")
    attachments = relationship("DailyReportAttachment", back_populates="daily_report", cascade="all, delete-orphan")

class WorkEntry(Base):
    __tablename__ = "work_entries"

    id = Column(Integer, primary_key=True, index=True)
    daily_report_id = Column(Integer, ForeignKey("daily_reports.id"), nullable=False)
    work_type = Column(String(100), nullable=False)  # 작업 유형
    description = Column(Text, nullable=False)  # 작업 내용
    start_time = Column(DateTime, nullable=False)  # 시작 시간
    end_time = Column(DateTime, nullable=False)  # 종료 시간
    worker_count = Column(Integer, nullable=False)  # 작업자 수
    equipment_used = Column(Text)  # 사용 장비
    materials_used = Column(Text)  # 사용 자재
    progress = Column(Float)  # 진행률
    notes = Column(Text)  # 비고
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계 설정
    daily_report = relationship("DailyReport", back_populates="work_entries")

class SafetyCheck(Base):
    __tablename__ = "safety_checks"

    id = Column(Integer, primary_key=True, index=True)
    daily_report_id = Column(Integer, ForeignKey("daily_reports.id"), nullable=False)
    check_type = Column(String(100), nullable=False)  # 점검 유형
    check_item = Column(String(200), nullable=False)  # 점검 항목
    status = Column(Boolean, nullable=False)  # 점검 결과
    issue = Column(Text)  # 문제점
    action_taken = Column(Text)  # 조치사항
    checked_by = Column(Integer, ForeignKey("users.id"))
    checked_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계 설정
    daily_report = relationship("DailyReport", back_populates="safety_checks")
    checker = relationship("User", back_populates="safety_checks")

class QualityCheck(Base):
    __tablename__ = "quality_checks"

    id = Column(Integer, primary_key=True, index=True)
    daily_report_id = Column(Integer, ForeignKey("daily_reports.id"), nullable=False)
    check_type = Column(String(100), nullable=False)  # 점검 유형
    check_item = Column(String(200), nullable=False)  # 점검 항목
    standard = Column(Text, nullable=False)  # 기준
    result = Column(Text, nullable=False)  # 결과
    status = Column(Boolean, nullable=False)  # 합격 여부
    issue = Column(Text)  # 문제점
    action_taken = Column(Text)  # 조치사항
    checked_by = Column(Integer, ForeignKey("users.id"))
    checked_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계 설정
    daily_report = relationship("DailyReport", back_populates="quality_checks")
    checker = relationship("User", back_populates="quality_checks")

class DailyReportAttachment(Base):
    __tablename__ = "daily_report_attachments"

    id = Column(Integer, primary_key=True, index=True)
    daily_report_id = Column(Integer, ForeignKey("daily_reports.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)
    file_type = Column(String(100))
    file_size = Column(Integer)
    description = Column(Text)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    # 관계 설정
    daily_report = relationship("DailyReport", back_populates="attachments")
    uploader = relationship("User", back_populates="daily_report_attachments") 