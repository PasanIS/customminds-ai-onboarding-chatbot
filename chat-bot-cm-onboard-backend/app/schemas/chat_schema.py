from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatMessageOut(BaseModel):
    id: int
    sender: str
    content: str
    message_metadata: Optional[str]
    created_at: datetime

class Config:
    orm_mode = True

class ChatResponse(BaseModel):
    reply: str
    saved: bool = False
    message: Optional[ChatMessageOut] = None