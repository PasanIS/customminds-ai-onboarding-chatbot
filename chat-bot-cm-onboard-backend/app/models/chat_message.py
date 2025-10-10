from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.core.database import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    message_metadata = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
