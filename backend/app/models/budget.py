from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, JSON, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.models.base import Base

class BudgetType(str, enum.Enum):
    INITIAL = "initial"  # 초기 예산
    REVISION = "revision"  # 수정 예산
    SUPPLEMENTARY = "supplementary"  # 보충 예산

class BudgetStatus(str, enum.Enum):
    DRAFT = "draft"  # 초안
    PENDING = "pending"  # 검토중
    APPROVED = "approved"  # 승인
    REJECTED = "rejected"  # 반려
    CANCELLED = "cancelled"  # 취소

class BudgetCategory(str, enum.Enum):
    LABOR = "labor"  # 인건비
    MATERIAL = "material"  # 자재비
    EQUIPMENT = "equipment"  # 장비비
    SUBCONTRACT = "subcontract"  # 하도급비
    INDIRECT = "indirect"  # 간접비
    OTHER = "other"  # 기타

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    budget_type = Column(Enum(BudgetType), nullable=False)
    budget_status = Column(Enum(BudgetStatus), nullable=False, default=BudgetStatus.DRAFT)
    version = Column(Integer, nullable=False, default=1)  # 예산 버전
    total_amount = Column(Float, nullable=False)  # 총 예산
    start_date = Column(DateTime, nullable=False)  # 예산 적용 시작일
    end_date = Column(DateTime, nullable=False)  # 예산 적용 종료일
    description = Column(Text)  # 예산 설명
    created_by = Column(Integer, ForeignKey("users.id"))
    approved_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = Column(JSON)

    # 관계 설정
    project = relationship("Project", back_populates="budgets")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_budgets")
    approver = relationship("User", foreign_keys=[approved_by], back_populates="approved_budgets")
    items = relationship("BudgetItem", back_populates="budget", cascade="all, delete-orphan")
    attachments = relationship("BudgetAttachment", back_populates="budget", cascade="all, delete-orphan")
    approvals = relationship("BudgetApproval", back_populates="budget", cascade="all, delete-orphan")

class BudgetItem(Base):
    __tablename__ = "budget_items"

    id = Column(Integer, primary_key=True, index=True)
    budget_id = Column(Integer, ForeignKey("budgets.id"), nullable=False)
    category = Column(Enum(BudgetCategory), nullable=False)
    subcategory = Column(String(100), nullable=False)  # 세부 항목
    description = Column(Text, nullable=False)  # 항목 설명
    amount = Column(Float, nullable=False)  # 예산 금액
    unit = Column(String(50))  # 단위
    quantity = Column(Float)  # 수량
    unit_price = Column(Float)  # 단가
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계 설정
    budget = relationship("Budget", back_populates="items")

class BudgetAttachment(Base):
    __tablename__ = "budget_attachments"

    id = Column(Integer, primary_key=True, index=True)
    budget_id = Column(Integer, ForeignKey("budgets.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)
    file_type = Column(String(100))
    file_size = Column(Integer)
    description = Column(Text)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    # 관계 설정
    budget = relationship("Budget", back_populates="attachments")
    uploader = relationship("User", back_populates="budget_attachments")

class BudgetApproval(Base):
    __tablename__ = "budget_approvals"

    id = Column(Integer, primary_key=True, index=True)
    budget_id = Column(Integer, ForeignKey("budgets.id"), nullable=False)
    approver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(BudgetStatus), nullable=False)
    comments = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계 설정
    budget = relationship("Budget", back_populates="approvals")
    approver = relationship("User", back_populates="budget_approvals")

class BudgetAlert(Base):
    __tablename__ = "budget_alerts"

    id = Column(Integer, primary_key=True, index=True)
    budget_id = Column(Integer, ForeignKey("budgets.id"), nullable=False)
    alert_type = Column(String(100), nullable=False)  # 알림 유형
    threshold = Column(Float, nullable=False)  # 임계값
    current_value = Column(Float, nullable=False)  # 현재값
    message = Column(Text, nullable=False)  # 알림 메시지
    is_active = Column(Boolean, default=True)  # 활성화 여부
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계 설정
    budget = relationship("Budget", back_populates="alerts") 