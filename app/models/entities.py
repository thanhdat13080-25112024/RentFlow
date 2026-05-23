from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
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

class ElectricityReading(Base):
    __tablename__ = "electricity_readings"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    month = Column(Integer)
    year = Column(Integer)
    old_reading = Column(Integer)
    new_reading = Column(Integer)
    unit_price = Column(Integer)

    room = relationship("Room", back_populates="readings")

class MonthlyBill(Base):
    __tablename__ = "monthly_bills"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    month = Column(Integer)
    year = Column(Integer)
    electricity_fee = Column(Integer)
    rent_fee = Column(Integer)
    service_fee = Column(Integer)
    total = Column(Integer)
    status = Column(String)  # "unpaid", "paid", "prepaid"
    prepaid_months = Column(String, nullable=True)
    paid_at = Column(DateTime, nullable=True)
    
    tenant_name = Column(String, nullable=True)
    move_in_date = Column(String, nullable=True)

    room = relationship("Room", back_populates="bills")

class Setting(Base):
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True)
    value = Column(String)
