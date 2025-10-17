from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    class Config:
        from_attributes = True

class ChatMessageOut(BaseModel):
    id: int
    session_id: Optional[str]
    sender: str
    content: str
    message_metadata: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    reply: str
    saved: bool = False
    message: Optional[ChatMessageOut] = None
    session_id: Optional[str] = None

    class Config:
        from_attributes = True