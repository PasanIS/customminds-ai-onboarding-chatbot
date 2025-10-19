from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey
from app.core.database import Base


class PharmacyInventory(Base):
    __tablename__ = "pharmacy_inventory"

    drug_id = Column(String(50), primary_key=True, nullable=False, index=True)
    drug_name = Column(String(100), nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)
    brand = Column(String(50), nullable=False, index=True)
    unit_price = Column(Integer, nullable=False)
    quantity_in_stock = Column(Integer, nullable=False)
    expiry_date = Column(DateTime, nullable=False)
    supplier_id = Column(String(50), ForeignKey("suppliers.supplier_id"), nullable=False, index=True)
    reorder_level = Column(Integer, nullable=False)
    location = Column(String(100), nullable=False, index=True)