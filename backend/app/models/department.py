from sqlalchemy import Column, String, Text, ForeignKey, Integer, DateTime, JSON, UUID, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from sqlalchemy.sql import func

from backend.app.models.base import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True, index=True)
    code = Column(String(50), nullable=False, unique=True, index=True)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=True)
    level = Column(Integer, nullable=False, default=1)
    description = Column(Text, nullable=True)
    headquarters_id = Column(UUID(as_uuid=True), ForeignKey("headquarters.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    parent = relationship("Department", remote_side=[id], backref="children")
    headquarters = relationship("Headquarters", back_populates="departments")
    users = relationship("User", back_populates="department", cascade="all, delete-orphan")
    contracts = relationship("Contract", back_populates="department")
    history = relationship("DepartmentHistory", back_populates="department")
    projects = relationship("Project", back_populates="department", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Department {self.name}>"

class DepartmentHistory(Base):
    __tablename__ = "department_history"

    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    action_type = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE
    previous_data = Column(JSON, nullable=True)
    new_data = Column(JSON, nullable=True)
    changed_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    department = relationship("Department", back_populates="history")
    user = relationship("User", back_populates="department_changes")

    def __repr__(self):
        return f"<DepartmentHistory {self.department_id} {self.action_type}>" 