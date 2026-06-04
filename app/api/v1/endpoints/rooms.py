from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models import ElectricityReading, MonthlyBill, Room, Setting
from app.schemas import RoomCreate, RoomHistoryRead, RoomRead, RoomUpdate
from app.services.billing import update_bill

router = APIRouter()

@router.get("/", response_model=List[RoomRead])
async def get_rooms(db: Session = Depends(get_db)):
    return db.query(Room).all()

@router.post("/", response_model=RoomRead, status_code=201)
async def create_room(data: RoomCreate, db: Session = Depends(get_db)):
    """Tạo phòng mới. Trả 409 nếu room_number đã tồn tại."""
    existing = db.query(Room).filter(Room.room_number == data.room_number).first()
    if existing:
        raise HTTPException(status_code=409, detail=f"Phòng {data.room_number} đã tồn tại")
    room = Room(
        room_number=data.room_number,
        rent_price=data.rent_price,
        service_fee=data.service_fee,
        deposit=data.deposit,
        electricity_type=data.electricity_type,
        fixed_electricity_fee=data.fixed_electricity_fee,
        is_occupied=False,
    )
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

@router.delete("/{room_id}")
async def delete_room(room_id: int, db: Session = Depends(get_db)):
    """Xoá phòng trống. Chặn nếu đang có khách (is_occupied)."""
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Không tìm thấy phòng")
    if room.is_occupied:
        raise HTTPException(status_code=400, detail="Phòng đang có khách. Vui lòng trả phòng trước khi xoá.")
    # Cascade delete electricity readings and bills
    db.query(ElectricityReading).filter(ElectricityReading.room_id == room_id).delete()
    db.query(MonthlyBill).filter(MonthlyBill.room_id == room_id).delete()
    db.delete(room)
    db.commit()
    return {"message": f"Đã xoá phòng {room.room_number}"}

@router.post("/update")
async def update_room(data: RoomUpdate, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == data.id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    room.room_number = data.room_number
    room.rent_price = data.rent_price
    room.service_fee = data.service_fee
    room.deposit = data.deposit
    room.contact_info = data.contact_info
    room.move_in_date = data.move_in_date
    room.electricity_type = data.electricity_type
    room.fixed_electricity_fee = data.fixed_electricity_fee
    # occupancy gắn với việc CÓ KHÁCH (contact_info), không phải có giá phòng.
    # Trước đây "rent + service > 0" khiến phòng trống đã cấu hình giá bị tính là đang thuê.
    room.is_occupied = bool(data.contact_info and str(data.contact_info).strip())
    
    if data.month and data.year:
        if data.old_reading is not None:
            reading = db.query(ElectricityReading).filter(
                ElectricityReading.room_id == room.id,
                ElectricityReading.month == data.month,
                ElectricityReading.year == data.year
            ).first()
            if reading:
                reading.old_reading = data.old_reading
            else:
                unit_price_setting = db.query(Setting).filter(Setting.key == "electricity_unit_price").first()
                unit_price = int(unit_price_setting.value) if unit_price_setting else 4000
                reading = ElectricityReading(
                    room_id=room.id, month=data.month, year=data.year,
                    old_reading=data.old_reading, new_reading=data.old_reading,
                    unit_price=unit_price
                )
                db.add(reading)
            db.flush()

        update_bill(db, room, data.month, data.year)
            
    db.commit()
    return {"message": "Cập nhật thông tin thành công"}

@router.post("/{room_id}/move-out")
async def move_out(room_id: int, db: Session = Depends(get_db)):
    """Dọn phòng: chuyển về trạng thái trống, xoá thông tin khách hiện tại.
    Hoá đơn lịch sử giữ nguyên (tenant_name đã được snapshot trên từng bill)."""
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    room.is_occupied = False
    room.contact_info = None
    room.move_in_date = None
    db.commit()
    return {"message": f"Đã dọn phòng {room.room_number}"}


@router.get("/{room_id}/history", response_model=List[RoomHistoryRead])
async def get_room_history(room_id: int, db: Session = Depends(get_db)):
    bills = db.query(MonthlyBill).filter(MonthlyBill.room_id == room_id).order_by(MonthlyBill.year.desc(), MonthlyBill.month.desc()).all()
    readings = db.query(ElectricityReading).filter(ElectricityReading.room_id == room_id).all()
    
    reading_map = {(r.year, r.month): r for r in readings}
    
    history = []
    for bill in bills:
        reading = reading_map.get((bill.year, bill.month))
        history.append({
            "month": bill.month,
            "year": bill.year,
            "tenant_name": bill.tenant_name,
            "rent_fee": bill.rent_fee,
            "service_fee": bill.service_fee,
            "electricity_fee": bill.electricity_fee,
            "total": bill.total,
            "status": bill.status,
            "paid_at": bill.paid_at,
            "old_reading": reading.old_reading if reading else 0,
            "new_reading": reading.new_reading if reading else 0,
            "usage": (reading.new_reading - reading.old_reading) if reading else 0
        })
    return history
