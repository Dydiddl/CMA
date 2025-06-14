from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base_class import Base

class ConstructionStatus(str, enum.Enum):
    PLANNING = "planning"  # 계획
    BIDDING = "bidding"  # 입찰
    CONTRACTED = "contracted"  # 계약
    IN_PROGRESS = "in_progress"  # 진행중
    COMPLETED = "completed"  # 완료
    SUSPENDED = "suspended"  # 중단
    TERMINATED = "terminated"  # 해지

class ConstructionType(str, enum.Enum):
    NEW_CONSTRUCTION = "new_construction"  # 신축
    RENOVATION = "renovation"  # 리모델링
    REPAIR = "repair"  # 보수
    DEMOLITION = "demolition"  # 철거

class Construction(Base):
    __tablename__ = "constructions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    construction_number = Column(String(50), unique=True, nullable=False, index=True)  # 공사번호
    description = Column(Text, nullable=True)
    
    # 공사 기본 정보
    type = Column(Enum(ConstructionType), nullable=False)
    status = Column(Enum(ConstructionStatus), default=ConstructionStatus.PLANNING, nullable=False)
    location = Column(String(500), nullable=False)  # 공사 위치
    area = Column(Float, nullable=True)  # 공사 면적(㎡)
    
    # 계약 정보
    contract_number = Column(String(100), nullable=True)  # 계약번호
    contract_date = Column(DateTime, nullable=True)  # 계약일
    contract_amount = Column(Float, nullable=True)  # 계약금액
    contract_period = Column(Integer, nullable=True)  # 계약기간(일)
    
    # 일정 정보
    start_date = Column(DateTime, nullable=True)  # 착공일
    planned_end_date = Column(DateTime, nullable=True)  # 예정 완료일
    actual_end_date = Column(DateTime, nullable=True)  # 실제 완료일
    
    # 비용 정보
    estimated_cost = Column(Float, nullable=True)  # 예상 비용
    actual_cost = Column(Float, nullable=True)  # 실제 비용
    payment_status = Column(String(50), nullable=True)  # 지급 상태
    
    # 관계 설정
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # 발주자
    client = relationship("User", foreign_keys=[client_id], back_populates="ordered_constructions")
    
    contractor_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # 수급자
    contractor = relationship("User", foreign_keys=[contractor_id], back_populates="contracted_constructions")
    
    supervisor_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # 감리자
    supervisor = relationship("User", foreign_keys=[supervisor_id], back_populates="supervised_constructions")
    
    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Construction {self.construction_number}>"

class ConstructionProgress(Base):
    __tablename__ = "construction_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    construction_id = Column(UUID(as_uuid=True), ForeignKey("constructions.id"), nullable=False)
    progress_date = Column(Date, nullable=False)
    progress_percentage = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    construction = relationship("Construction", back_populates="progress")

    def __repr__(self):
        return f"<ConstructionProgress {self.construction_id} {self.progress_date}>"

class ConstructionDocument(Base):
    __tablename__ = "construction_documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    construction_id = Column(UUID(as_uuid=True), ForeignKey("constructions.id"), nullable=False)
    document_type = Column(String(50), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_name = Column(String(200), nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String(100), nullable=False)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    construction = relationship("Construction", back_populates="documents")
    uploader = relationship("User", back_populates="uploaded_documents")

    def __repr__(self):
        return f"<ConstructionDocument {self.file_name}>"

class ConstructionHistory(Base):
    __tablename__ = "construction_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    construction_id = Column(UUID(as_uuid=True), ForeignKey("constructions.id"), nullable=False)
    action_type = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE
    previous_data = Column(JSON, nullable=True)
    new_data = Column(JSON, nullable=True)
    changed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    construction = relationship("Construction", back_populates="history")
    user = relationship("User", back_populates="construction_changes")

    def __repr__(self):
        return f"<ConstructionHistory {self.construction_id} {self.action_type}>" 