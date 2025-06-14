from sqlalchemy import Column, String, Text, ForeignKey, DateTime, JSON, UUID, Integer, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from backend.app.models.base import Base

class User(Base):
    """
    사용자 정보를 저장하는 테이블
    사용자의 기본 정보와 인증 정보를 관리합니다.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # 사용자 고유 식별자
    email = Column(String, unique=True, index=True, nullable=False)  # 이메일 주소 (고유)
    username = Column(String, unique=True, index=True, nullable=False)  # 사용자 이름 (고유)
    hashed_password = Column(String, nullable=False)  # 암호화된 비밀번호
    is_active = Column(Boolean(), default=True)  # 계정 활성화 상태
    is_superuser = Column(Boolean(), default=False)
    role = Column(String, default="USER")  # 사용자 역할 (USER, ADMIN 등)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 계정 생성 일시
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())  # 정보 수정 일시
    department_id = Column(Integer, ForeignKey("departments.id"))

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    history = relationship("UserHistory", back_populates="user")
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
    owned_projects = relationship("Project", back_populates="owner", foreign_keys="[Project.owner_id]")
    contracts = relationship("Contract", back_populates="manager")
    approved_amendments = relationship("ContractAmendment", back_populates="approver")
    created_documents = relationship("Document", foreign_keys="[Document.created_by]", back_populates="creator")
    approved_documents = relationship("Document", foreign_keys="[Document.approved_by]", back_populates="approver")
    document_versions = relationship("DocumentVersion", back_populates="creator")
    document_tags = relationship("DocumentTag", back_populates="creator")
    document_comments = relationship("DocumentComment", back_populates="creator")
    shared_documents = relationship("DocumentShare", foreign_keys="[DocumentShare.user_id]", back_populates="user")
    created_shares = relationship("DocumentShare", foreign_keys="[DocumentShare.created_by]", back_populates="creator")
    department = relationship("Department", back_populates="users")
    department_changes = relationship("DepartmentHistory", back_populates="user")
    managed_contracts = relationship("Contract", back_populates="manager")
    contract_changes = relationship("ContractHistory", back_populates="user")
    managed_constructions = relationship("Construction", back_populates="manager")
    uploaded_documents = relationship("ConstructionDocument", back_populates="uploader")
    construction_changes = relationship("ConstructionHistory", back_populates="user")
    vendor_changes = relationship("VendorHistory", back_populates="user")
    headquarters_changes = relationship("HeadquartersHistory", back_populates="user")
    tasks = relationship("Task", back_populates="assignee")
    notifications = relationship("Notification", back_populates="user")
    notification_stats = relationship("NotificationStats", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    full_name = Column(String)
    phone_number = Column(String)
    position = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<UserProfile {self.user_id}>"

class UserHistory(Base):
    __tablename__ = "user_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
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