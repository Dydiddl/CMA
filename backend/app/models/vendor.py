from sqlalchemy import String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from app.models.base import Base

class Vendor(Base):
    """
    거래처(공급업체) 정보를 관리하는 모델
    """
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

    def __repr__(self):
        return f"<Vendor {self.company_name}>"

class VendorHistory(Base):
    """
    거래처 정보 변경 이력을 관리하는 모델
    """
    vendor_id: Mapped[UUID] = mapped_column(ForeignKey('vendor.id'), nullable=False)
    action_type: Mapped[str] = mapped_column(String(50), nullable=False)  # 작업 유형
    previous_data: Mapped[dict] = mapped_column(JSON, nullable=True)  # 변경 전 데이터
    new_data: Mapped[dict] = mapped_column(JSON, nullable=True)  # 변경 후 데이터
    changed_by: Mapped[UUID] = mapped_column(ForeignKey('user.id'), nullable=False)  # 변경 수행자 ID

    # 관계 설정
    vendor = relationship("Vendor", back_populates="history")
    changer = relationship("User", back_populates="vendor_changes")

    def __repr__(self):
        return f"<VendorHistory {self.vendor_id} - {self.action_type}>" 