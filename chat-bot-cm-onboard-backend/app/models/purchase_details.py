from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey, DECIMAL
from app.core.database import Base


class PurchaseDetails(Base):
    __tablename__ = "purchase_details"

    purchase_detail_id = Column(Integer, primary_key=True, autoincrement=True)
    purchase_id = Column(String(50), ForeignKey("purchases.purchase_id"), nullable=False, index=True)
    drug_id = Column(String(50), ForeignKey("pharmacy_inventory.drug_id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    unit_cost = Column(DECIMAL(10,2), nullable=False)
    subtotal = Column(DECIMAL(10,2), nullable=False)