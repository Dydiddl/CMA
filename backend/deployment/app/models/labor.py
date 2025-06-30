from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import BaseModel

class Labor(BaseModel):
    __tablename__ = "labors"

    name = Column(String)
    phone = Column(String)
    id_number = Column(String, unique=True)  # 주민번호 또는 외국인등록번호
    bank_name = Column(String)
    bank_account = Column(String)
    daily_wage = Column(Float)
    status = Column(String)  # 재직중, 퇴사 등
    contract_id = Column(Integer, ForeignKey("contracts.id"))

    # 관계 설정
    contract = relationship("Contract", back_populates="labors")
    work_logs = relationship("WorkLog", back_populates="labor")

class WorkLog(BaseModel):
    __tablename__ = "work_logs"

    labor_id = Column(Integer, ForeignKey("labors.id"))
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