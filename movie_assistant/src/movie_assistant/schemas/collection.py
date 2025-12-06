from pydantic import BaseModel, Field
from fastapi import Query
from uuid import UUID


class CollectionBase(BaseModel):
    name: str = Field(..., min_length=3)


class ViewCollection(CollectionBase):
    id: UUID


class GetCollection(BaseModel):
    id: UUID = None
