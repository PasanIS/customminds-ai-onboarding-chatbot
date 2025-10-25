from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey, DECIMAL
from app.core.database import Base


class Customers(Base):
    __tablename__ = "customers"

    customer_id = Column(String(50), primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(20), index=True)
    email = Column(String(100), unique=True, index=True)
    address = Column(Text, nullable=False)