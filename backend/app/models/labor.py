from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.models.base import Base

class WorkerType(enum.Enum):
    CONSTRUCTION_WORKER = "construction_worker"  # 건설 노무직
    SKILLED_WORKER = "skilled_worker"  # 숙련공
    SUPERVISOR = "supervisor"  # 감독
    ENGINEER = "engineer"  # 기술자
    ADMINISTRATOR = "administrator"  # 행정직

class WorkerStatus(enum.Enum):
    ACTIVE = "active"  # 재직
    ON_LEAVE = "on_leave"  # 휴직
    RESIGNED = "resigned"  # 퇴직
    SUSPENDED = "suspended"  # 정직

class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    worker_type = Column(Enum(WorkerType), nullable=False)
    status = Column(Enum(WorkerStatus), default=WorkerStatus.ACTIVE)
    phone = Column(String(20))
    email = Column(String(100))
    address = Column(String(200))
    emergency_contact = Column(String(100))
    emergency_phone = Column(String(20))
    hire_date = Column(DateTime, nullable=False)
    resignation_date = Column(DateTime)
    hourly_rate = Column(Float)
    bank_account = Column(String(50))
    bank_name = Column(String(50))
    bank_holder = Column(String(100))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    attendance_records = relationship("AttendanceRecord", back_populates="worker")
    safety_trainings = relationship("SafetyTraining", back_populates="worker")
    certifications = relationship("Certification", back_populates="worker")
    payroll_records = relationship("PayrollRecord", back_populates="worker")

class AttendanceRecord(Base):
    __tablename__ = "attendance_records"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    check_in = Column(DateTime)
    check_out = Column(DateTime)
    work_hours = Column(Float)
    overtime_hours = Column(Float)
    status = Column(String(50))  # 정상, 지각, 조퇴, 결근 등
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    worker = relationship("Worker", back_populates="attendance_records")

class SafetyTraining(Base):
    __tablename__ = "safety_trainings"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=False)
    training_date = Column(DateTime, nullable=False)
    training_type = Column(String(100), nullable=False)
    trainer = Column(String(100))
    location = Column(String(200))
    duration = Column(Float)  # 시간 단위
    score = Column(Float)
    passed = Column(Boolean)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    worker = relationship("Worker", back_populates="safety_trainings")

class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=False)
    name = Column(String(100), nullable=False)
    issuing_organization = Column(String(200))
    issue_date = Column(DateTime, nullable=False)
    expiry_date = Column(DateTime)
    certificate_number = Column(String(100))
    status = Column(String(50))  # 유효, 만료, 취소 등
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    worker = relationship("Worker", back_populates="certifications")

class PayrollRecord(Base):
    __tablename__ = "payroll_records"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=False)
    payment_date = Column(DateTime, nullable=False)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    regular_hours = Column(Float)
    overtime_hours = Column(Float)
    regular_pay = Column(Float)
    overtime_pay = Column(Float)
    deductions = Column(Float)
    net_pay = Column(Float)
    payment_method = Column(String(50))
    status = Column(String(50))  # 미지급, 지급완료 등
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    worker = relationship("Worker", back_populates="payroll_records") 