from sqlalchemy.orm import Session
from app.models.models import Setting, Room

def init_data(db: Session):
    # Cài đặt mặc định
    default_settings = [
        {"key": "electricity_unit_price", "value": "3500"},
        {"key": "bank_account", "value": "123456789"},
        {"key": "bank_name", "value": "Vietcombank"},
        {"key": "account_holder", "value": "NGUYỄN VĂN VÍ DỤ"}
    ]
    
    for s in default_settings:
        if not db.query(Setting).filter(Setting.key == s["key"]).first():
            db.add(Setting(**s))

    # Danh sách phòng ví dụ
    rooms_data = [
        {
            "room_number": "101",
            "rent_price": 2000000,
            "service_fee": 100000,
            "deposit": 2000000,
            "contact_info": "Nguyễn Văn A - 0901234567",
            "move_in_date": "2024-01-01",
            "electricity_type": "meter",
            "is_occupied": True
        },
        {
            "room_number": "102",
            "rent_price": 2200000,
            "service_fee": 100000,
            "deposit": 2200000,
            "contact_info": None,
            "move_in_date": None,
            "electricity_type": "meter",
            "is_occupied": False
        },
        {
            "room_number": "201",
            "rent_price": 2500000,
            "service_fee": 150000,
            "deposit": 2500000,
            "contact_info": "Trần Thị B - 0988888888",
            "move_in_date": "2024-02-15",
            "electricity_type": "fixed",
            "fixed_electricity_fee": 200000,
            "is_occupied": True
        },
        {
            "room_number": "202",
            "rent_price": 2500000,
            "service_fee": 150000,
            "deposit": 0,
            "contact_info": None,
            "move_in_date": None,
            "electricity_type": "meter",
            "is_occupied": False
        },
        {
            "room_number": "301",
            "rent_price": 3000000,
            "service_fee": 200000,
            "deposit": 3000000,
            "contact_info": "Lê Văn C - 0912345678",
            "move_in_date": "2024-03-01",
            "electricity_type": "meter",
            "is_occupied": True
        }
    ]

    for r in rooms_data:
        if not db.query(Room).filter(Room.room_number == r["room_number"]).first():
            db.add(Room(**r))
    
    db.commit()
