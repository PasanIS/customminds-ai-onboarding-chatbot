from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey, DECIMAL
from app.core.database import Base


class SalesDetails(Base):
    __tablename__ = "sales_details"

    sale_detail_id = Column(Integer, primary_key=True, autoincrement=True)
    sale_id = Column(String(50), ForeignKey("sales.sale_id"), nullable=False, index=True)
    drug_id = Column(String(50), ForeignKey("pharmacy_inventory.drug_id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10,2), nullable=False)
    subtotal = Column(DECIMAL(10,2), nullable=False)