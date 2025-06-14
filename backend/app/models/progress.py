from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON, UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from backend.app.models.base import Base

class Progress(Base):
    __tablename__ = "progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    progress_date = Column(DateTime, nullable=False)
    progress_percentage = Column(Float, nullable=False)
    status = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    project = relationship("Project", back_populates="progresses")

    def __repr__(self):
        return f"<Progress {self.project_id} {self.progress_date}>" 