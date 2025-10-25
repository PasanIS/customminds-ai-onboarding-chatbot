from datetime import datetime
from sqlalchemy import Integer, Column, String, Text, DateTime
from app.core.database import Base


class HumanReview(Base):
    __tablename__ = "human_reviews"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(50), nullable=False)
    user_query = Column(Text, nullable=False)
    status = Column(String(100), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)