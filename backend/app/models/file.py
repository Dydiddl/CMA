from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(100), nullable=False)
    file_size = Column(Integer, nullable=False)  # 바이트 단위
    description = Column(Text, nullable=True)
    
    # 관계 설정
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    project = relationship("Project", back_populates="files")
    
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    task = relationship("Task", back_populates="files")
    
    uploader_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    uploader = relationship("User", back_populates="uploaded_files")
    
    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<File {self.original_filename}>" 