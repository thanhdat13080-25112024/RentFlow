from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.entities import Room, ElectricityReading, Setting
from app.schemas.data_transfer_objects import ElectricityInput
from app.services.billing import update_bill

router = APIRouter()

@router.post("/")
async def update_electricity(data: ElectricityInput, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == data.room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    if room.electricity_type == "fixed":
        return {"message": "Phòng này sử dụng điện khoán"}

    unit_price_setting = db.query(Setting).filter(Setting.key == "electricity_unit_price").first()
    unit_price = int(unit_price_setting.value) if unit_price_setting else 4000

    old_reading = 0
    last_reading = db.query(ElectricityReading).filter(
        ElectricityReading.room_id == data.room_id,
        (ElectricityReading.year < data.year) | 
        ((ElectricityReading.year == data.year) & (ElectricityReading.month < data.month))
    ).order_by(ElectricityReading.year.desc(), ElectricityReading.month.desc()).first()
    
    if last_reading:
        old_reading = last_reading.new_reading

    if data.new_reading < old_reading:
        raise HTTPException(status_code=400, detail=f"Số mới ({data.new_reading}) không được nhỏ hơn số cũ ({old_reading})")

    reading = db.query(ElectricityReading).filter(
        ElectricityReading.room_id == data.room_id,
        ElectricityReading.month == data.month,
        ElectricityReading.year == data.year
    ).first()

    if reading:
        reading.new_reading = data.new_reading
        reading.old_reading = old_reading
    else:
        reading = ElectricityReading(
            room_id=data.room_id,
            month=data.month,
            year=data.year,
            old_reading=old_reading,
            new_reading=data.new_reading,
            unit_price=unit_price
        )
        db.add(reading)
    
    db.commit()
    
    update_bill(db, room, data.month, data.year)
    
    return {"message": "Cập nhật số điện thành công"}
