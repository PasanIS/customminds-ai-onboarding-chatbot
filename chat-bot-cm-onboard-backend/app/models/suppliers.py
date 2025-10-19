from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey
from app.core.database import Base


class Suppliers(Base):
    __tablename__ = "suppliers"

    supplier_id = Column(String(50), primary_key=True, nullable=False, index=True)
    supplier_name = Column(String(50), nullable=False, index=True)
    contact_person = Column(String(50), nullable=False, index=True)
    phone_number = Column(String(50), nullable=False, index=True)
    email = Column(String(50), nullable=False, index=True)
    address = Column(String(50), nullable=False, index=True)