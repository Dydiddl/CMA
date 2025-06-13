from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Client(Base):
    """
    거래처(발주처) 정보를 관리하는 모델
    """
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    business_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=True)
    representative_name: Mapped[str] = mapped_column(String(100), nullable=True)
    contact_person: Mapped[str] = mapped_column(String(100), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    address: Mapped[str] = mapped_column(Text, nullable=True)

    def __repr__(self):
        return f"<Client {self.company_name}>" 