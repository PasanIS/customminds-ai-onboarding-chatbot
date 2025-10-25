from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey, DECIMAL
from app.core.database import Base


class Sales(Base):
    __tablename__ = "sales"

    sale_id = Column(String(50), primary_key=True, nullable=False, index=True)
    customer_id = Column(String(50), ForeignKey("customers.customer_id"), nullable=False, index=True)
    emp_id = Column(String(50), ForeignKey("employees.emp_id"), nullable=False, index=True)
    sale_date = Column(DateTime, default=func.now(), nullable=False)
    total_sale = Column(DECIMAL(10,2), nullable=False)
