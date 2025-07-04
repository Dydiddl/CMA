from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Text, Date, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.database import Base
import uuid

class Labor(Base):
    __tablename__ = "labors"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    phone = Column(String)
    id_number = Column(String, unique=True)  # 주민번호 또는 외국인등록번호
    bank_name = Column(String)
    bank_account = Column(String)
    daily_wage = Column(Float)
    status = Column(String)  # 재직중, 퇴사 등
    contract_id = Column(String, ForeignKey("contracts.id"), nullable=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=True, comment="사용자 ID")
    
    # 소프트 삭제
    deleted_at = Column(DateTime, nullable=True, comment="삭제일")
    is_deleted = Column(Boolean, default=False, nullable=False, comment="삭제 여부")

    # 관계 설정 - 문자열로 참조하여 순환 참조 방지
    contract = relationship("Contract", back_populates="labors")
    project = relationship("Project", back_populates="labors")
    work_logs = relationship("WorkLog", back_populates="labor")

    @property
    def total_cost(self):
        """총 비용 계산"""
        return self.daily_wage if self.daily_wage else 0.0

    def __repr__(self):
        return f"<Labor(id={self.id}, name={self.name}, daily_wage={self.daily_wage})>"

class WorkLog(Base):
    __tablename__ = "work_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    labor_id = Column(String, ForeignKey("labors.id"))
    work_date = Column(Date)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    work_hours = Column(Float)
    daily_wage = Column(Float)
    total_amount = Column(Float)
    description = Column(Text)
    status = Column(String)  # 미지급, 지급완료 등

    # 관계 설정
    labor = relationship("Labor", back_populates="work_logs") 