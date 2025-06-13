from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from .base import Base

class Document(Base):
    """
    계약 관련 문서를 관리하는 모델
    """
    contract_id: Mapped[UUID] = mapped_column(ForeignKey('contract.id'), nullable=False)
    document_type: Mapped[str] = mapped_column(String(50), nullable=False)  # contract, invoice, receipt, report
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)  # 파일 크기 (bytes)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)  # 파일 형식
    uploaded_by: Mapped[UUID] = mapped_column(ForeignKey('user.id'), nullable=False)

    # 관계 설정
    contract = relationship("Contract", back_populates="documents")
    uploader = relationship("User", back_populates="uploaded_documents")

    def __repr__(self):
        return f"<Document {self.file_name}>" 