from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

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
    
    # Thông tin khách tại thời điểm này
    tenant_name = Column(String, nullable=True)
    move_in_date = Column(String, nullable=True)

    room = relationship("Room", back_populates="bills")

class Setting(Base):
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True)
    value = Column(String)

# Dữ liệu khởi tạo (Seed Data)
def init_data(db):
    # Cài đặt mặc định
    default_settings = [
        {"key": "electricity_unit_price", "value": "4000"},
        {"key": "bank_account", "value": ""},
        {"key": "bank_name", "value": "MB"},
        {"key": "account_holder", "value": ""}
    ]
    
    for s in default_settings:
        if not db.query(Setting).filter(Setting.key == s["key"]).first():
            db.add(Setting(**s))

    # Danh sách 18 phòng
    rooms_data = [
        {"room_number": "101", "rent_price": 0, "service_fee": 300000, "deposit": 1000000, "electricity_type": "fixed", "fixed_electricity_fee": 200000, "is_occupied": True},
        {"room_number": "201", "rent_price": 1500000, "service_fee": 300000, "deposit": 1000000, "electricity_type": "meter", "is_occupied": False},
        {"room_number": "202", "rent_price": 0, "service_fee": 300000, "deposit": 1000000, "electricity_type": "meter", "is_occupied": False},
        {"room_number": "203", "rent_price": 1000000, "service_fee": 250000, "deposit": 1000000, "electricity_type": "meter", "is_occupied": False},
        {"room_number": "301", "rent_price": 0, "service_fee": 300000, "deposit": 0, "electricity_type": "meter", "is_occupied": False},
        {"room_number": "302", "rent_price": 1000000, "service_fee": 250000, "deposit": 1000000, "electricity_type": "meter", "is_occupied": False},
        {"room_number": "303", "rent_price": 1000000, "service_fee": 300000, "deposit": 0, "electricity_type": "meter", "is_occupied": False},
        {"room_number": "401", "rent_price": 0, "service_fee": 400000, "deposit": 1000000, "electricity_type": "meter", "is_occupied": False},
        {"room_number": "402", "rent_price": 1000000, "service_fee": 250000, "deposit": 1000000, "electricity_type": "meter", "is_occupied": False},
        {"room_number": "403", "rent_price": 0, "service_fee": 300000, "deposit": 1000000, "electricity_type": "meter", "is_occupied": False},
        {"room_number": "501", "rent_price": 0, "service_fee": 300000, "deposit": 1000000, "electricity_type": "meter", "is_occupied": False},
        {"room_number": "502", "rent_price": 0, "service_fee": 300000, "deposit": 0, "electricity_type": "meter", "is_occupied": False},
        {"room_number": "503", "rent_price": 1000000, "service_fee": 300000, "deposit": 1000000, "electricity_type": "meter", "is_occupied": False},
        {"room_number": "601", "rent_price": 1500000, "service_fee": 700000, "deposit": 0, "electricity_type": "meter", "is_occupied": False},
        {"room_number": "602", "rent_price": 0, "service_fee": 250000, "deposit": 1000000, "electricity_type": "meter", "is_occupied": False},
        {"room_number": "603", "rent_price": 1000000, "service_fee": 300000, "deposit": 1000000, "electricity_type": "meter", "is_occupied": False},
        {"room_number": "701", "rent_price": 0, "service_fee": 300000, "deposit": 500000, "electricity_type": "meter", "is_occupied": False},
        {"room_number": "702", "rent_price": 1000000, "service_fee": 300000, "deposit": 1000000, "electricity_type": "meter", "is_occupied": False},
    ]

    for r in rooms_data:
        if not db.query(Room).filter(Room.room_number == r["room_number"]).first():
            db.add(Room(**r))
    
    db.commit()
