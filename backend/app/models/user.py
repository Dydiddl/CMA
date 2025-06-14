from sqlalchemy import Column, String, Text, ForeignKey, DateTime, JSON, UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=True)
    position = Column(String(50), nullable=True)
    status = Column(String(20), nullable=False, default="ACTIVE")  # ACTIVE, INACTIVE, SUSPENDED
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    department = relationship("Department", back_populates="users")
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    history = relationship("UserHistory", back_populates="user")
    managed_contracts = relationship("Contract", back_populates="manager")
    managed_constructions = relationship("Construction", back_populates="manager")
    uploaded_documents = relationship("ConstructionDocument", back_populates="uploader")
    contract_changes = relationship("ContractHistory", back_populates="user")
    construction_changes = relationship("ConstructionHistory", back_populates="user")
    department_changes = relationship("DepartmentHistory", back_populates="user")
    vendor_changes = relationship("VendorHistory", back_populates="user")
    headquarters_changes = relationship("HeadquartersHistory", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    profile_image = Column(String(500), nullable=True)
    language = Column(String(10), nullable=False, default="ko")
    timezone = Column(String(50), nullable=False, default="Asia/Seoul")
    notification_settings = Column(JSON, nullable=True)
    theme_settings = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<UserProfile {self.user_id}>"

class UserHistory(Base):
    __tablename__ = "user_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    action_type = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE
    previous_data = Column(JSON, nullable=True)
    new_data = Column(JSON, nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="history")

    def __repr__(self):
        return f"<UserHistory {self.user_id} {self.action_type}>" 