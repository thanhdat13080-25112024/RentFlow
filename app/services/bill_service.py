from sqlalchemy.orm import Session
from datetime import datetime
from app.models.models import Room, ElectricityReading, MonthlyBill

def update_bill(db: Session, room: Room, month: int, year: int):
    reading = db.query(ElectricityReading).filter(
        ElectricityReading.room_id == room.id,
        ElectricityReading.month == month,
        ElectricityReading.year == year
    ).first()

    elec_fee = 0
    if room.electricity_type == "fixed":
        elec_fee = room.fixed_electricity_fee
    elif reading:
        elec_fee = (reading.new_reading - reading.old_reading) * reading.unit_price

    bill = db.query(MonthlyBill).filter(
        MonthlyBill.room_id == room.id,
        MonthlyBill.month == month,
        MonthlyBill.year == year
    ).first()

    total = room.rent_price + room.service_fee + elec_fee

    if bill:
        if bill.status == "unpaid": # Chỉ cập nhật nếu chưa thanh toán
            bill.electricity_fee = elec_fee
            bill.rent_fee = room.rent_price
            bill.service_fee = room.service_fee
            bill.total = total
            bill.tenant_name = room.contact_info
            bill.move_in_date = room.move_in_date
    else:
        bill = MonthlyBill(
            room_id=room.id,
            month=month,
            year=year,
            electricity_fee=elec_fee,
            rent_fee=room.rent_price,
            service_fee=room.service_fee,
            total=total,
            status="unpaid",
            tenant_name=room.contact_info,
            move_in_date=room.move_in_date
        )
        db.add(bill)
    db.commit()
