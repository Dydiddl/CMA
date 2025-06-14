from sqlalchemy import String, Text, Date, Numeric, Integer, ForeignKey, JSON, Column, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from backend.app.models.base import Base
import uuid
from datetime import datetime

class Headquarters(Base):
    """
    본사의 기본 정보를 관리하는 모델
    """
    __tablename__ = "headquarters"
    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)  # 본사명
    business_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)  # 사업자등록번호
    address: Mapped[str] = mapped_column(Text, nullable=False)  # 주소
    phone: Mapped[str] = mapped_column(String(20), nullable=True)  # 대표 전화번호
    email: Mapped[str] = mapped_column(String(100), nullable=True)  # 대표 이메일
    established_date: Mapped[Date] = mapped_column(Date, nullable=True)  # 설립일
    representative_name: Mapped[str] = mapped_column(String(100), nullable=True)  # 대표자명
    description: Mapped[str] = mapped_column(Text, nullable=True)  # 설명
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계 설정
    details = relationship("HeadquartersDetail", back_populates="headquarters")
    facilities = relationship("HeadquartersFacility", back_populates="headquarters")
    history = relationship("HeadquartersHistory", back_populates="headquarters")
    departments = relationship("Department", back_populates="headquarters")

    def __repr__(self):
        return f"<Headquarters {self.name}>"

class HeadquartersDetail(Base):
    """
    본사의 상세 정보를 관리하는 모델
    """
    __tablename__ = "headquarters_detail"
    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    headquarters_id: Mapped[UUID] = mapped_column(ForeignKey('headquarters.id'), nullable=False)
    industry: Mapped[str] = mapped_column(String(100), nullable=True)  # 업종
    business_type: Mapped[str] = mapped_column(String(100), nullable=True)  # 사업 유형
    employee_count: Mapped[int] = mapped_column(Integer, nullable=True)  # 직원 수
    annual_revenue: Mapped[float] = mapped_column(Numeric(15, 2), nullable=True)  # 연간 매출
    main_business: Mapped[str] = mapped_column(Text, nullable=True)  # 주요 사업

    # 관계 설정
    headquarters = relationship("Headquarters", back_populates="details")

    def __repr__(self):
        return f"<HeadquartersDetail {self.headquarters_id}>"

class HeadquartersFacility(Base):
    """
    본사의 시설 정보를 관리하는 모델
    """
    __tablename__ = "headquarters_facility"
    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    headquarters_id: Mapped[UUID] = mapped_column(ForeignKey('headquarters.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)  # 시설명
    type: Mapped[str] = mapped_column(String(50), nullable=False)  # 시설 유형
    location: Mapped[str] = mapped_column(String(100), nullable=True)  # 위치
    capacity: Mapped[int] = mapped_column(Integer, nullable=True)  # 수용 인원
    status: Mapped[str] = mapped_column(String(50), nullable=True)  # 상태
    description: Mapped[str] = mapped_column(Text, nullable=True)  # 설명

    # 관계 설정
    headquarters = relationship("Headquarters", back_populates="facilities")

    def __repr__(self):
        return f"<HeadquartersFacility {self.name}>"

class HeadquartersHistory(Base):
    """
    본사 정보 변경 이력을 관리하는 모델
    """
    __tablename__ = "headquarters_history"
    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    headquarters_id: Mapped[UUID] = mapped_column(ForeignKey('headquarters.id'), nullable=False)
    action_type: Mapped[str] = mapped_column(String(50), nullable=False)  # 작업 유형
    previous_data: Mapped[dict] = mapped_column(JSON, nullable=True)  # 변경 전 데이터
    new_data: Mapped[dict] = mapped_column(JSON, nullable=True)  # 변경 후 데이터
    changed_by: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)  # 변경 수행자 ID

    # 관계 설정
    headquarters = relationship("Headquarters", back_populates="history")
    user = relationship("User", back_populates="headquarters_changes")

    def __repr__(self):
        return f"<HeadquartersHistory {self.headquarters_id} - {self.action_type}>" 