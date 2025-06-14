from sqlalchemy import Column, String, Text, ForeignKey, Integer, DateTime, JSON, UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.models.base import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    code = Column(String(50), nullable=False, unique=True)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=True)
    level = Column(Integer, nullable=False, default=1)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    parent = relationship("Department", remote_side=[id], backref="children")
    users = relationship("User", back_populates="department")
    history = relationship("DepartmentHistory", back_populates="department")

    def __repr__(self):
        return f"<Department {self.name}>"

class DepartmentHistory(Base):
    __tablename__ = "department_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False)
    action_type = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE
    previous_data = Column(JSON, nullable=True)
    new_data = Column(JSON, nullable=True)
    changed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    department = relationship("Department", back_populates="history")
    user = relationship("User", back_populates="department_changes")

    def __repr__(self):
        return f"<DepartmentHistory {self.department_id} {self.action_type}>" 