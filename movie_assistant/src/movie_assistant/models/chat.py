from sqlalchemy import Column, String, ForeignKey, func, DateTime, Boolean, Text, JSON
from movie_assistant.database.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid


class ChatSession(Base):
    __tablename__ = "chat_session"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        index=True,
        default=uuid.uuid4,
    )
    user_id = Column(ForeignKey("user.id"), nullable=False)
    title = Column(String, unique=True, nullable=False)
    summary = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )


class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        index=True,
        default=uuid.uuid4,
    )
    session_id = Column(ForeignKey("chat_session.id"), nullable=False)
    chat_role = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    citation = Column(JSON, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
