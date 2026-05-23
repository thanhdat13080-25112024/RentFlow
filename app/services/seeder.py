from sqlalchemy.orm import Session
from app.models import ElectricityReading, MonthlyBill, Room, Setting
from datetime import datetime, timedelta

def seed_initial_data(db: Session):
    # 1. Cài đặt mặc định
    default_settings = [
        {"key": "electricity_unit_price", "value": "3500"},
        {"key": "bank_account", "value": "1028711116666"},
        {"key": "bank_name", "value": "MB"},
        {"key": "account_holder", "value": "NGUYEN VAN ADMIN"}
    ]
    
    for s in default_settings:
        if not db.query(Setting).filter(Setting.key == s["key"]).first():
            db.add(Setting(**s))

    # 2. Danh sách 12 phòng ví dụ (3 tầng)
    rooms_data = [
        # Tầng 1
        {"room_number": "101", "rent_price": 2500000, "service_fee": 150000, "deposit": 2500000, "contact_info": "Nguyễn Văn An - 0901234567", "move_in_date": "2024-01-10", "electricity_type": "meter", "is_occupied": True},
        {"room_number": "102", "rent_price": 2500000, "service_fee": 150000, "deposit": 2500000, "contact_info": "Trần Thị Bình - 0988776655", "move_in_date": "2024-02-15", "electricity_type": "meter", "is_occupied": True},
        {"room_number": "103", "rent_price": 2800000, "service_fee": 150000, "deposit": 2800000, "contact_info": "Lê Văn Cường - 0911223344", "move_in_date": "2024-03-01", "electricity_type": "meter", "is_occupied": True},
        {"room_number": "104", "rent_price": 2800000, "service_fee": 150000, "deposit": 0, "contact_info": None, "move_in_date": None, "electricity_type": "meter", "is_occupied": False},
        
        # Tầng 2
        {"room_number": "201", "rent_price": 3000000, "service_fee": 200000, "deposit": 3000000, "contact_info": "Phạm Minh Đức - 0933445566", "move_in_date": "2024-01-05", "electricity_type": "meter", "is_occupied": True},
        {"room_number": "202", "rent_price": 3000000, "service_fee": 200000, "deposit": 3000000, "contact_info": "Hoàng Thị Em - 0944556677", "move_in_date": "2024-04-20", "electricity_type": "fixed", "fixed_electricity_fee": 200000, "is_occupied": True},
        {"room_number": "203", "rent_price": 3200000, "service_fee": 200000, "deposit": 3200000, "contact_info": "Đặng Văn Giang - 0955667788", "move_in_date": "2024-05-01", "electricity_type": "meter", "is_occupied": True},
        {"room_number": "204", "rent_price": 3200000, "service_fee": 200000, "deposit": 0, "contact_info": None, "move_in_date": None, "electricity_type": "meter", "is_occupied": False},

        # Tầng 3
        {"room_number": "301", "rent_price": 3500000, "service_fee": 250000, "deposit": 3500000, "contact_info": "Bùi Thị Hoa - 0966778899", "move_in_date": "2024-02-10", "electricity_type": "meter", "is_occupied": True},
        {"room_number": "302", "rent_price": 3500000, "service_fee": 250000, "deposit": 3500000, "contact_info": "Lý Văn Hùng - 0977889900", "move_in_date": "2024-03-15", "electricity_type": "meter", "is_occupied": True},
        {"room_number": "303", "rent_price": 4000000, "service_fee": 250000, "deposit": 0, "contact_info": None, "move_in_date": None, "electricity_type": "meter", "is_occupied": False},
        {"room_number": "304", "rent_price": 4000000, "service_fee": 250000, "deposit": 0, "contact_info": None, "move_in_date": None, "electricity_type": "meter", "is_occupied": False},
    ]

    for r in rooms_data:
        if not db.query(Room).filter(Room.room_number == r["room_number"]).first():
            db.add(Room(**r))
    
    db.commit()

    # 3. Thêm dữ liệu lịch sử (Hoá đơn & Số điện) cho 3 tháng gần nhất
    now = datetime.now()
    rooms = db.query(Room).filter(Room.is_occupied == True).all()
    
    # Kiểm tra xem đã có dữ liệu hoá đơn chưa để tránh lặp
    if db.query(MonthlyBill).count() == 0:
        for i in range(2, -1, -1): # Cách đây 2 tháng, 1 tháng, và tháng này
            target_date = now - timedelta(days=i*30)
            m, y = target_date.month, target_date.year
            
            for room in rooms:
                # Giả lập số điện
                old_r = 100 + (i * 50)
                new_r = old_r + 40 + (room.id % 20)
                usage = new_r - old_r
                elec_fee = usage * 3500 if room.electricity_type == "meter" else (room.fixed_electricity_fee or 0)
                
                # Lưu số điện
                reading = ElectricityReading(
                    room_id=room.id, month=m, year=y,
                    old_reading=old_r, new_reading=new_r, unit_price=3500
                )
                db.add(reading)
                
                # Tạo hoá đơn
                total = room.rent_price + room.service_fee + elec_fee
                status = "paid" if i > 0 else "unpaid" # Các tháng trước đã đóng, tháng này chưa
                
                bill = MonthlyBill(
                    room_id=room.id, month=m, year=y,
                    rent_fee=room.rent_price, service_fee=room.service_fee,
                    electricity_fee=elec_fee, total=total, status=status,
                    tenant_name=room.contact_info.split(" - ")[0] if room.contact_info else "N/A",
                    move_in_date=room.move_in_date,
                    paid_at=datetime.now() if status == "paid" else None
                )
                db.add(bill)
        
        db.commit()
