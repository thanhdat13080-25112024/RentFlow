from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String, unique=True, index=True)
    rent_price = Column(Integer, default=0)
    service_fee = Column(Integer, default=0)
    deposit = Column(Integer, default=0)
    contact_info = Column(String, nullable=True)
    move_in_date = Column(String, nullable=True)
    electricity_type = Column(String)  # "meter" hoặc "fixed"
    fixed_electricity_fee = Column(Integer, default=0)
    is_occupied = Column(Boolean, default=False)

    readings = relationship("ElectricityReading", back_populates="room")
    bills = relationship("MonthlyBill", back_populates="room")
