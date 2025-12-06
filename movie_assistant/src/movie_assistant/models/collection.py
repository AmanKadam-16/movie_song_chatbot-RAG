from sqlalchemy import Column, String, ForeignKey, func, DateTime, Boolean, Text, JSON
from movie_assistant.database.database import Base
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy.vector import VECTOR
import uuid


class Collection(Base):
    __tablename__ = "collection"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        index=True,
        default=uuid.uuid4,
    )
    name = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )


class Document(Base):
    __tablename__ = "document"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        index=True,
        default=uuid.uuid4,
    )
    name = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )


class CollectionDocument(Base):
    __tablename__ = "collection_document"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        index=True,
        default=uuid.uuid4,
    )
    collection_id = Column(ForeignKey("collection.id"), nullable=False)
    document_id = Column(ForeignKey("document.id"), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )


class ChunkEmbedding(Base):
    __tablename__ = "chunk_embedding"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        index=True,
        default=uuid.uuid4,
    )
    collection_document_id = Column(
        ForeignKey("collection_document.id"), nullable=False
    )
    embedding = Column(VECTOR(4096), nullable=False)
    chunk = Column(Text, nullable=False)
    chunk_metadata = Column(JSON, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
