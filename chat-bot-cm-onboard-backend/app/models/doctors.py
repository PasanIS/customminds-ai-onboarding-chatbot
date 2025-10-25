from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey, DECIMAL
from app.core.database import Base


class Doctors(Base):
    __tablename__ = "doctors"

    doctor_id = Column(String(50), primary_key=True, index=True)
    doctor_name = Column(String(50), nullable=False)
    specialization = Column(String(50), nullable=False)
    phone = Column(String(20), unique=True, index=True)
    hospital = Column(String(100), nullable=False)