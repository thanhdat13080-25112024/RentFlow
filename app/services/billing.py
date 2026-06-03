from typing import Optional

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import ElectricityReading, MonthlyBill, Room, Setting


def get_unit_price(db: Session) -> int:
    """Giá điện/kWh dùng chung: ưu tiên Setting trong DB, fallback về config.

    Tránh hardcode rải rác (trước đây có 4000 ở endpoint và 3500 ở seeder)."""
    s = db.query(Setting).filter(Setting.key == "electricity_unit_price").first()
    if s and str(s.value).strip().isdigit():
        return int(s.value)
    return settings.DEFAULT_ELECTRICITY_UNIT_PRICE


def compute_bill_fields(room: Room, reading: Optional[ElectricityReading]) -> dict:
    """Tính các khoản tiền cho 1 phòng/tháng — THUẦN, KHÔNG đụng DB.

    Dùng chung cho cả hiển thị (các endpoint GET, không ghi) lẫn update_bill (ghi)."""
    if room.electricity_type == "fixed":
        elec_fee = room.fixed_electricity_fee or 0
    elif reading:
        elec_fee = (reading.new_reading - reading.old_reading) * reading.unit_price
    else:
        elec_fee = 0
    return {
        "electricity_fee": elec_fee,
        "rent_fee": room.rent_price,
        "service_fee": room.service_fee,
        "total": room.rent_price + room.service_fee + elec_fee,
    }


def update_bill(db: Session, room: Room, month: int, year: int):
    """Tạo/cập nhật MonthlyBill cho 1 phòng/tháng — CÓ ghi DB + commit.

    Chỉ gọi từ các luồng GHI (mark-paid, nhập điện, sửa phòng). Các endpoint GET
    KHÔNG gọi hàm này nữa — chúng tính ảo bằng compute_bill_fields để không ghi DB
    khi chỉ xem. Chỉ cập nhật bill khi status == 'unpaid' (không ghi đè bill đã
    thu / đóng trước)."""
    reading = db.query(ElectricityReading).filter(
        ElectricityReading.room_id == room.id,
        ElectricityReading.month == month,
        ElectricityReading.year == year,
    ).first()

    fields = compute_bill_fields(room, reading)

    bill = db.query(MonthlyBill).filter(
        MonthlyBill.room_id == room.id,
        MonthlyBill.month == month,
        MonthlyBill.year == year,
    ).first()

    if bill:
        if bill.status == "unpaid":  # Chỉ cập nhật nếu chưa thanh toán
            bill.electricity_fee = fields["electricity_fee"]
            bill.rent_fee = fields["rent_fee"]
            bill.service_fee = fields["service_fee"]
            bill.total = fields["total"]
            bill.tenant_name = room.contact_info
            bill.move_in_date = room.move_in_date
    else:
        bill = MonthlyBill(
            room_id=room.id,
            month=month,
            year=year,
            status="unpaid",
            tenant_name=room.contact_info,
            move_in_date=room.move_in_date,
            **fields,
        )
        db.add(bill)
    db.commit()
