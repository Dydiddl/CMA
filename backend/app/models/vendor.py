from sqlalchemy import String, Text, JSON, Column, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from backend.app.models.base import Base
from datetime import datetime
import uuid

class Vendor(Base):
    """
    거래처(공급업체) 정보를 관리하는 모델
    """
    __tablename__ = "vendors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)  # 회사명
    business_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)  # 사업자등록번호
    representative_name: Mapped[str] = mapped_column(String(100), nullable=False)  # 대표자명
    contact_person: Mapped[str] = mapped_column(String(100), nullable=True)  # 담당자명
    phone: Mapped[str] = mapped_column(String(20), nullable=True)  # 연락처
    email: Mapped[str] = mapped_column(String(255), nullable=True)  # 이메일
    address: Mapped[str] = mapped_column(Text, nullable=True)  # 주소
    bank_info: Mapped[dict] = mapped_column(JSON, nullable=True)  # 은행 정보
    documents: Mapped[dict] = mapped_column(JSON, nullable=True)  # 문서 메타데이터

    # 관계 설정
    contracts = relationship("Contract", back_populates="vendor")
    history = relationship("VendorHistory", back_populates="vendor")

    def __repr__(self):
        return f"<Vendor {self.company_name}>"

class VendorHistory(Base):
    __tablename__ = "vendor_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vendor_id = Column(UUID(as_uuid=True), ForeignKey("vendors.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    action_type = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE
    previous_data = Column(JSON, nullable=True)
    new_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    vendor = relationship("Vendor", back_populates="history")
    user = relationship("User", back_populates="vendor_changes")

    def __repr__(self):
        return f"<VendorHistory {self.vendor_id} {self.action_type}>" 