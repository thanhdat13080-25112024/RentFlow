from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import ElectricityReading, MonthlyBill, Room, Setting


def seed_initial_data(db: Session):
    up = settings.DEFAULT_ELECTRICITY_UNIT_PRICE
    # 1. Cài đặt mặc định
    default_settings = [
        {"key": "electricity_unit_price", "value": str(up)},
        {"key": "bank_account", "value": "1028711116666"},
        {"key": "bank_name", "value": "MB"},
        {"key": "account_holder", "value": "NGUYEN VAN ADMIN"}
    ]

    for s in default_settings:
        if not db.query(Setting).filter(Setting.key == s["key"]).first():
            db.add(Setting(**s))

    # 2. Danh sách 20 phòng ví dụ (4 tầng) — đa dạng giá thuê, loại điện,
    #    ngày vào ở (2023→2025) và xen kẽ phòng trống.
    rooms_data = [
        # ── Tầng 1 ──
        {"room_number": "101", "rent_price": 2500000, "service_fee": 150000, "deposit": 2500000, "contact_info": "Nguyễn Văn An - 0901234567", "move_in_date": "2023-06-10", "electricity_type": "meter", "is_occupied": True},
        {"room_number": "102", "rent_price": 2600000, "service_fee": 150000, "deposit": 2600000, "contact_info": "Trần Thị Bình - 0988776655", "move_in_date": "2024-02-15", "electricity_type": "meter", "is_occupied": True},
        {"room_number": "103", "rent_price": 2800000, "service_fee": 150000, "deposit": 2800000, "contact_info": "Lê Văn Cường - 0911223344", "move_in_date": "2024-03-01", "electricity_type": "fixed", "fixed_electricity_fee": 180000, "is_occupied": True},
        {"room_number": "104", "rent_price": 2800000, "service_fee": 150000, "deposit": 0, "contact_info": None, "move_in_date": None, "electricity_type": "meter", "is_occupied": False},
        {"room_number": "105", "rent_price": 2400000, "service_fee": 120000, "deposit": 2400000, "contact_info": "Vũ Thị Dung - 0902345678", "move_in_date": "2025-01-05", "electricity_type": "meter", "is_occupied": True},

        # ── Tầng 2 ──
        {"room_number": "201", "rent_price": 3000000, "service_fee": 200000, "deposit": 3000000, "contact_info": "Phạm Minh Đức - 0933445566", "move_in_date": "2023-11-05", "electricity_type": "meter", "is_occupied": True},
        {"room_number": "202", "rent_price": 3000000, "service_fee": 200000, "deposit": 3000000, "contact_info": "Hoàng Thị Em - 0944556677", "move_in_date": "2024-04-20", "electricity_type": "fixed", "fixed_electricity_fee": 200000, "is_occupied": True},
        {"room_number": "203", "rent_price": 3200000, "service_fee": 200000, "deposit": 3200000, "contact_info": "Đặng Văn Giang - 0955667788", "move_in_date": "2024-05-01", "electricity_type": "meter", "is_occupied": True},
        {"room_number": "204", "rent_price": 3200000, "service_fee": 200000, "deposit": 0, "contact_info": None, "move_in_date": None, "electricity_type": "meter", "is_occupied": False},
        {"room_number": "205", "rent_price": 3100000, "service_fee": 200000, "deposit": 3100000, "contact_info": "Đỗ Thị Hồng - 0903456789", "move_in_date": "2024-08-12", "electricity_type": "meter", "is_occupied": True},

        # ── Tầng 3 ──
        {"room_number": "301", "rent_price": 3500000, "service_fee": 250000, "deposit": 3500000, "contact_info": "Bùi Thị Hoa - 0966778899", "move_in_date": "2023-02-10", "electricity_type": "meter", "is_occupied": True},
        {"room_number": "302", "rent_price": 3500000, "service_fee": 250000, "deposit": 3500000, "contact_info": "Lý Văn Hùng - 0977889900", "move_in_date": "2024-03-15", "electricity_type": "fixed", "fixed_electricity_fee": 220000, "is_occupied": True},
        {"room_number": "303", "rent_price": 4000000, "service_fee": 250000, "deposit": 0, "contact_info": None, "move_in_date": None, "electricity_type": "meter", "is_occupied": False},
        {"room_number": "304", "rent_price": 3800000, "service_fee": 250000, "deposit": 3800000, "contact_info": "Ngô Thị Kim - 0904567890", "move_in_date": "2024-12-01", "electricity_type": "meter", "is_occupied": True},
        {"room_number": "305", "rent_price": 3600000, "service_fee": 250000, "deposit": 3600000, "contact_info": "Trịnh Văn Long - 0915678901", "move_in_date": "2025-03-20", "electricity_type": "meter", "is_occupied": True},

        # ── Tầng 4 ──
        {"room_number": "401", "rent_price": 4200000, "service_fee": 300000, "deposit": 4200000, "contact_info": "Mai Thị Lan - 0926789012", "move_in_date": "2024-06-18", "electricity_type": "meter", "is_occupied": True},
        {"room_number": "402", "rent_price": 4200000, "service_fee": 300000, "deposit": 4200000, "contact_info": "Phan Văn Minh - 0937890123", "move_in_date": "2024-09-09", "electricity_type": "fixed", "fixed_electricity_fee": 250000, "is_occupied": True},
        {"room_number": "403", "rent_price": 4500000, "service_fee": 300000, "deposit": 0, "contact_info": None, "move_in_date": None, "electricity_type": "meter", "is_occupied": False},
        {"room_number": "404", "rent_price": 4500000, "service_fee": 300000, "deposit": 4500000, "contact_info": "Dương Thị Nga - 0948901234", "move_in_date": "2025-02-14", "electricity_type": "meter", "is_occupied": True},
    ]

    for r in rooms_data:
        if not db.query(Room).filter(Room.room_number == r["room_number"]).first():
            db.add(Room(**r))

    db.commit()

    # 3. Thêm dữ liệu lịch sử (Hoá đơn & Số điện) cho 3 tháng gần nhất
    now = datetime.now()
    rooms = db.query(Room).filter(Room.is_occupied == True).order_by(Room.room_number).all()

    # Trạng thái tháng hiện tại — trộn để dashboard đa dạng:
    # ~1/3 chưa thu, ~1/3 đã thu, ~1/3 đóng trước (xoay vòng theo phòng).
    current_status_cycle = ["unpaid", "paid", "prepaid", "paid", "unpaid", "prepaid", "paid"]

    def next_month(m, y):
        return (1, y + 1) if m == 12 else (m + 1, y)

    # Kiểm tra xem đã có dữ liệu hoá đơn chưa để tránh lặp
    if db.query(MonthlyBill).count() == 0:
        for i in range(5, -1, -1):  # 5 tháng trước → tháng này (đủ 6 cột biểu đồ)
            target_date = now - timedelta(days=i * 30)
            m, y = target_date.month, target_date.year

            for idx, room in enumerate(rooms):
                # Giả lập số điện (biến thiên theo phòng & theo tháng)
                old_r = 100 + (i * 50) + (room.id % 10) * 3
                new_r = old_r + 35 + (room.id % 25)
                usage = new_r - old_r
                elec_fee = usage * up if room.electricity_type == "meter" else (room.fixed_electricity_fee or 0)

                # Lưu số điện
                reading = ElectricityReading(
                    room_id=room.id, month=m, year=y,
                    old_reading=old_r, new_reading=new_r, unit_price=up
                )
                db.add(reading)

                # Trạng thái: các tháng trước đã đóng; tháng này trộn nhiều loại.
                if i > 0:
                    status = "paid"
                else:
                    status = current_status_cycle[idx % len(current_status_cycle)]

                # Đóng trước → ghi danh sách (các) tháng tới đã trả.
                prepaid_months = None
                if status == "prepaid":
                    nm, ny = next_month(m, y)
                    prepaid_months = str(nm)

                # Tạo hoá đơn
                total = room.rent_price + room.service_fee + elec_fee
                # paid_at trải đều vài ngày gần đây để "Hoạt động gần đây" sinh động
                paid_at = None
                if status in ("paid", "prepaid"):
                    paid_at = now - timedelta(days=(i * 28) + (idx % 7))

                bill = MonthlyBill(
                    room_id=room.id, month=m, year=y,
                    rent_fee=room.rent_price, service_fee=room.service_fee,
                    electricity_fee=elec_fee, total=total, status=status,
                    prepaid_months=prepaid_months,
                    tenant_name=room.contact_info.split(" - ")[0] if room.contact_info else "N/A",
                    move_in_date=room.move_in_date,
                    paid_at=paid_at
                )
                db.add(bill)

        db.commit()
