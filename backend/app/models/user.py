from sqlalchemy import String, Boolean, Column
from sqlalchemy.orm import relationship
from ..db.database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False, default="user")
    department = Column(String(50), nullable=True)
    phone = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<User {self.email}>" 