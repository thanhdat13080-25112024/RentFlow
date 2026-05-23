from sqlalchemy.orm import Session
from app.models.models import Setting, Room

def init_data(db: Session):
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
