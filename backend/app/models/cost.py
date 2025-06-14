from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base_class import Base

class CostType(str, enum.Enum):
    """비용 유형"""
    LABOR = "labor"           # 노무비
    MATERIAL = "material"     # 재료비
    EQUIPMENT = "equipment"   # 장비비
    SUBCONTRACT = "subcontract"  # 하도급비
    INDIRECT = "indirect"     # 경비
    OTHER = "other"           # 기타비용

class PaymentStatus(str, enum.Enum):
    """지급 상태"""
    PENDING = "pending"       # 대기중
    APPROVED = "approved"     # 승인됨
    PAID = "paid"            # 지급완료
    REJECTED = "rejected"     # 거절됨
    CANCELLED = "cancelled"   # 취소됨

class CostCategory(str, enum.Enum):
    """비용 카테고리"""
    # 노무비 카테고리
    WAGES = "wages"                    # 기본급
    OVERTIME = "overtime"            # 시간외수당
    SAFETY_ALLOWANCE = "safety_allowance"          # 안전수당
    MEAL_ALLOWANCE = "meal_allowance"          # 식대
    ACCOMMODATION = "accommodation"          # 숙식비
    INSURANCE = "insurance"          # 4대보험
    
    # 재료비 카테고리
    CEMENT = "cement"                    # 시멘트
    REBAR = "rebar"                    # 철근
    AGGREGATE = "aggregate"                    # 골재
    CONCRETE = "concrete"                    # 콘크리트
    STEEL = "steel"                    # 강재
    TIMBER = "timber"                    # 목재
    CONSUMABLES = "consumables"                    # 소모품
    MATERIAL_TRANSPORT = "material_transport"                    # 자재운반비
    
    # 장비비 카테고리
    CRANE = "crane"                    # 크레인
    EXCAVATOR = "excavator"                    # 굴삭기
    TRUCK = "truck"                    # 운반차량
    GENERATOR = "generator"                    # 발전기
    EQUIPMENT_MAINTENANCE = "equipment_maintenance"                    # 장비유지보수
    FUEL = "fuel"                    # 연료비
    
    # 하도급비 카테고리
    CONSTRUCTION = "construction"                    # 전문공사
    MECHANICAL = "mechanical"                    # 기계설비
    ELECTRICAL = "electrical"                    # 전기공사
    PLUMBING = "plumbing"                    # 배관공사
    CONSULTING = "consulting"                    # 용역
    
    # 경비 카테고리
    SITE_MANAGEMENT = "site_management"                    # 현장관리비
    SAFETY_MANAGEMENT = "safety_management"                    # 안전관리비
    QUALITY_MANAGEMENT = "quality_management"                    # 품질관리비
    ENVIRONMENTAL_MANAGEMENT = "environmental_management"                    # 환경관리비
    UTILITIES = "utilities"                    # 수도광열비
    COMMUNICATION = "communication"                    # 통신비
    OFFICE_SUPPLIES = "office_supplies"                    # 사무용품
    TRAVEL = "travel"                    # 출장비
    
    # 기타 카테고리
    OTHER = "other"                    # 기타비용

class BudgetStatus(str, enum.Enum):
    DRAFT = "draft"  # 초안
    PENDING = "pending"  # 검토중
    APPROVED = "approved"  # 승인됨
    REJECTED = "rejected"  # 거절됨
    CANCELLED = "cancelled"  # 취소됨

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)
    labor_amount = Column(Float, nullable=False)
    material_amount = Column(Float, nullable=False)
    equipment_amount = Column(Float, nullable=False)
    subcontract_amount = Column(Float, nullable=False)
    indirect_amount = Column(Float, nullable=False)
    status = Column(Enum(BudgetStatus), default=BudgetStatus.DRAFT)
    description = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"))
    approved_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = Column(JSON)

    # 관계 설정
    project = relationship("Project", back_populates="budgets")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_budgets")
    approver = relationship("User", foreign_keys=[approved_by], back_populates="approved_budgets")
    changes = relationship("BudgetChange", back_populates="budget", cascade="all, delete-orphan")

class BudgetChange(Base):
    __tablename__ = "budget_changes"

    id = Column(Integer, primary_key=True, index=True)
    budget_id = Column(Integer, ForeignKey("budgets.id"), nullable=False)
    change_type = Column(String(50), nullable=False)  # increase/decrease
    amount = Column(Float, nullable=False)
    reason = Column(Text, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON)

    # 관계 설정
    budget = relationship("Budget", back_populates="changes")
    creator = relationship("User", back_populates="budget_changes")

class CostAnalysis(Base):
    __tablename__ = "cost_analyses"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    analysis_date = Column(DateTime, nullable=False)
    total_cost = Column(Float, nullable=False)
    labor_cost = Column(Float, nullable=False)
    material_cost = Column(Float, nullable=False)
    equipment_cost = Column(Float, nullable=False)
    subcontract_cost = Column(Float, nullable=False)
    indirect_cost = Column(Float, nullable=False)
    labor_ratio = Column(Float, nullable=False)
    material_ratio = Column(Float, nullable=False)
    equipment_ratio = Column(Float, nullable=False)
    subcontract_ratio = Column(Float, nullable=False)
    indirect_ratio = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON)

    # 관계 설정
    project = relationship("Project", back_populates="cost_analyses")

class CostAlert(Base):
    __tablename__ = "cost_alerts"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    alert_type = Column(String(50), nullable=False)  # budget_exceeded, unusual_cost, etc.
    message = Column(Text, nullable=False)
    severity = Column(String(20), nullable=False)  # high, medium, low
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime)
    metadata = Column(JSON)

    # 관계 설정
    project = relationship("Project", back_populates="cost_alerts")

class Cost(Base):
    """비용 모델"""
    __tablename__ = "costs"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    cost_type = Column(Enum(CostType), nullable=False)
    category = Column(Enum(CostCategory), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(Text)
    payment_date = Column(DateTime)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    payment_method = Column(String(50))
    payment_reference = Column(String(100))
    invoice_number = Column(String(100))
    invoice_date = Column(DateTime)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    created_by = Column(Integer, ForeignKey("users.id"))
    approved_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = Column(JSON)  # 추가 메타데이터

    # 관계
    project = relationship("Project", back_populates="costs")
    vendor = relationship("Vendor", back_populates="costs")
    department = relationship("Department", back_populates="costs")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_costs")
    approver = relationship("User", foreign_keys=[approved_by], back_populates="approved_costs")
    attachments = relationship("CostAttachment", back_populates="cost", cascade="all, delete-orphan")
    approvals = relationship("CostApproval", back_populates="cost", cascade="all, delete-orphan")

class CostAttachment(Base):
    """비용 첨부파일 모델"""
    __tablename__ = "cost_attachments"

    id = Column(Integer, primary_key=True, index=True)
    cost_id = Column(Integer, ForeignKey("costs.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)
    file_type = Column(String(100))
    file_size = Column(Integer)
    description = Column(Text)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    # 관계
    cost = relationship("Cost", back_populates="attachments")
    uploader = relationship("User", back_populates="cost_attachments")

class CostApproval(Base):
    """비용 승인 모델"""
    __tablename__ = "cost_approvals"

    id = Column(Integer, primary_key=True, index=True)
    cost_id = Column(Integer, ForeignKey("costs.id"), nullable=False)
    approver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 관계
    cost = relationship("Cost", back_populates="approvals")
    approver = relationship("User", back_populates="cost_approvals") 