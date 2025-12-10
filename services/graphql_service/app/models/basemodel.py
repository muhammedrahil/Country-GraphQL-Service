import uuid
from sqlalchemy import (
    Column,
    String,
    DateTime,
    func,
)
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base
from app.enumarates.utils import StatusEnum


class BaseModel(Base):
    __abstract__ = True  # Prevents SQLAlchemy from creating a table for this class

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = Column(String(255), default=StatusEnum.ACTIVE.value)
    created_at = Column(DateTime, default=func.current_timestamp(), nullable=False)
    updated_at = Column(
        DateTime,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False,
    )
    deleted_at = Column(DateTime, nullable=True)
