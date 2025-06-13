from datetime import datetime
from typing import Any
from sqlalchemy.orm import as_declarative, declared_attr, Mapped, mapped_column
from sqlalchemy import DateTime
from uuid import uuid4, UUID

@as_declarative()
class Base:
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() 