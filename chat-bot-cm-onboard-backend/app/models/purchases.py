from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey, DECIMAL
from app.core.database import Base


class Purchases(Base):
    __tablename__ = "purchases"

    purchase_id = Column(String(50), primary_key=True, nullable=False, index=True)
    supplier_id = Column(String(10),
                         ForeignKey("suppliers.supplier_id"),
                         nullable=False)
    emp_id = Column(String(50),
                        ForeignKey("employees.emp_id"),
                        nullable=False)
    purchase_date = Column(DateTime, default=func.now(), nullable=False)
    total_cost = Column(DECIMAL(10,2), nullable=False)


