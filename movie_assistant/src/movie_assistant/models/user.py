from sqlalchemy import Column, String, func, DateTime, Boolean
from movie_assistant.database.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid


class User(Base):
    __tablename__ = "user"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        index=True,
        default=uuid.uuid4,
    )
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
