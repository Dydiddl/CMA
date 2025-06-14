from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON, UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from backend.app.models.base import Base

class FinancialRecord(Base):
    __tablename__ = "financial_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    record_date = Column(DateTime, nullable=False)
    record_type = Column(String(50), nullable=False)  # income, expense
    amount = Column(Float, nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    payment_method = Column(String(50), nullable=True)
    payment_status = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    project = relationship("Project", back_populates="financial_records")

    def __repr__(self):
        return f"<FinancialRecord {self.project_id} {self.record_date}>" 