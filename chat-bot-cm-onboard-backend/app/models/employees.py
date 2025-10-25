from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey, DECIMAL
from app.core.database import Base


class Employees(Base):
    __tablename__ = "employees"

    emp_id = Column(String(50), primary_key=True, index=True)
    emp_name = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False)
    phone = Column(String(20), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    salary = Column(DECIMAL(10,2), nullable=False)