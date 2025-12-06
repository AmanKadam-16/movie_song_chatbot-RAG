from pydantic import BaseModel
from uuid import UUID


class ChatInput(BaseModel):
    session_id: UUID
    prompt: str
