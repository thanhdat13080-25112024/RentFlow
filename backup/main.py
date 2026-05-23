from fastapi import FastAPI, Depends, Request, HTTPException, Query, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
import io
import csv

from database import engine, Base, SessionLocal, get_db
from models import Room, ElectricityReading, MonthlyBill, Setting, init_data

# Khởi tạo database
Base.metadata.create_all(bind=engine)
# Seed data
with SessionLocal() as db:
    init_data(db)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Models cho Pydantic
class ElectricityInput(BaseModel):
    room_id: int
    month: int
    year: int
    new_reading: int

class PaidInput(BaseModel):
    room_id: int
    month: int
    year: int

class PrepaidInput(BaseModel):
    room_id: int
    months: List[int]
    year: int

class SettingUpdate(BaseModel):
    key: str
    value: str

class RoomUpdate(BaseModel):
    id: int
    room_number: str
    rent_price: int
    service_fee: int
    deposit: int
    contact_info: Optional[str]
    move_in_date: Optional[str]
    electricity_type: str
    fixed_electricity_fee: int
    is_occupied: bool
    month: Optional[int] = None
    year: Optional[int] = None
    old_reading: Optional[int] = None

@app.get("/api/revenue/summary")
async def get_revenue_summary(db: Session = Depends(get_db)):
    # Tìm tất cả các cặp (tháng, năm) duy nhất có trong database
    bill_periods = db.query(MonthlyBill.month, MonthlyBill.year).distinct().all()
    reading_periods = db.query(ElectricityReading.month, ElectricityReading.year).distinct().all()
    
    # Gộp tất cả các chu kỳ lại để đồng bộ hóa hóa đơn
    all_periods = set(bill_periods) | set(reading_periods)
    
    # Thêm tháng 4/2026 và hiện tại nếu chưa có
    now = datetime.now()
    all_periods.add((now.month, now.year))
    all_periods.add((4, 2026))

    rooms = db.query(Room).all()
    for m, y in all_periods:
        for room in rooms:
            update_bill(db, room, m, y)

    results = db.query(
        MonthlyBill.year,
        MonthlyBill.month,
        db.func.sum(MonthlyBill.electricity_fee).label("total_elec"),
        db.func.sum(MonthlyBill.service_fee).label("total_service"),
        db.func.sum(MonthlyBill.rent_fee).label("total_rent"),
        db.func.sum(MonthlyBill.total).label("total_revenue")
    ).group_by(MonthlyBill.year, MonthlyBill.month).order_by(MonthlyBill.year.desc(), MonthlyBill.month.desc()).all()
    
    return [
        {
            "year": r.year,
            "month": r.month,
            "total_elec": int(r.total_elec or 0),
            "total_service": int(r.total_service or 0),
            "total_rent": int(r.total_rent or 0),
            "total_revenue": int(r.total_revenue or 0)
        } for r in results
    ]

@app.post("/api/import-csv")
async def import_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        content = await file.read()
        stream = io.StringIO(content.decode("utf-8-sig")) # Handle BOM
        reader = csv.DictReader(stream)
        
        # Lấy giá điện
        unit_price_setting = db.query(Setting).filter(Setting.key == "electricity_unit_price").first()
        unit_price = int(unit_price_setting.value) if unit_price_setting else 4000

        import_count = 0
        for row in reader:
            room_number = row.get("Phòng")
            month = int(row.get("Tháng", 0))
            year = int(row.get("Năm", 0))
            
            if not room_number or not month or not year:
                continue
                
            room = db.query(Room).filter(Room.room_number == room_number).first()
            if not room:
                continue

            # 1. Cập nhật thông tin phòng (Master Data)
            room.contact_info = row.get("Khách Thuê", room.contact_info)
            room.move_in_date = row.get("Ngày Vào", room.move_in_date)
            room.rent_price = int(row.get("Tiền Phòng", room.rent_price))
            room.service_fee = int(row.get("Dịch Vụ", room.service_fee))
            room.is_occupied = True if (room.rent_price + room.service_fee > 0) else False
            
            # 2. Xử lý số điện
            old_r = row.get("Điện Cũ")
            new_r = row.get("Điện Mới")
            elec_fee = 0
            
            if old_r is not None and new_r is not None and old_r != "" and new_r != "":
                old_r = int(old_r)
                new_r = int(new_r)
                elec_fee = (new_r - old_r) * unit_price
                
                reading = db.query(ElectricityReading).filter(
                    ElectricityReading.room_id == room.id,
                    ElectricityReading.month == month,
                    ElectricityReading.year == year
                ).first()
                
                if reading:
                    reading.old_reading = old_r
                    reading.new_reading = new_r
                else:
                    db.add(ElectricityReading(
                        room_id=room.id, month=month, year=year,
                        old_reading=old_r, new_reading=new_r, unit_price=unit_price
                    ))
            elif room.electricity_type == "fixed":
                elec_fee = room.fixed_electricity_fee

            # 3. Tạo/Cập nhật hóa đơn
            status_map = {"Da thu": "paid", "Chua thu": "unpaid", "Dong truoc": "prepaid"}
            raw_status = row.get("Trạng Thái", "Chua thu")
            status = status_map.get(raw_status, "unpaid")
            
            bill = db.query(MonthlyBill).filter(
                MonthlyBill.room_id == room.id,
                MonthlyBill.month == month,
                MonthlyBill.year == year
            ).first()
            
            total = room.rent_price + room.service_fee + elec_fee
            
            if bill:
                bill.tenant_name = room.contact_info
                bill.move_in_date = room.move_in_date
                bill.rent_fee = room.rent_price
                bill.service_fee = room.service_fee
                bill.electricity_fee = elec_fee
                bill.total = total
                bill.status = status
                if status != "unpaid" and not bill.paid_at:
                    bill.paid_at = datetime.now()
            else:
                db.add(MonthlyBill(
                    room_id=room.id, month=month, year=year,
                    rent_fee=room.rent_price, service_fee=room.service_fee,
                    electricity_fee=elec_fee, total=total, status=status,
                    tenant_name=room.contact_info, move_in_date=room.move_in_date,
                    paid_at=datetime.now() if status != "unpaid" else None
                ))
            
            import_count += 1
            
        db.commit()
        return {"message": f"Đã import thành công {import_count} dòng dữ liệu"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, month: int = None, year: int = None):
    now = datetime.now()
    if month is None: month = now.month
    if year is None: year = now.year
    return templates.TemplateResponse(
        request=request, name="index.html", context={"month": month, "year": year}
    )

@app.get("/api/bills")
async def get_bills(month: int, year: int, db: Session = Depends(get_db)):
    rooms = db.query(Room).all()
    results = []
    
    for room in rooms:
        # Tự động đồng bộ hóa đơn để đảm bảo dữ liệu doanh thu luôn đúng
        update_bill(db, room, month, year)
        
        # Tìm hóa đơn của tháng này
        bill = db.query(MonthlyBill).filter(
            MonthlyBill.room_id == room.id,
            MonthlyBill.month == month,
            MonthlyBill.year == year
        ).first()
        
        # Tìm chỉ số điện
        reading = db.query(ElectricityReading).filter(
            ElectricityReading.room_id == room.id,
            ElectricityReading.month == month,
            ElectricityReading.year == year
        ).first()
        
        display_old = 0
        if reading:
            display_old = reading.old_reading
        else:
            last_reading = db.query(ElectricityReading).filter(
                ElectricityReading.room_id == room.id,
                (ElectricityReading.year < year) | 
                ((ElectricityReading.year == year) & (ElectricityReading.month < month))
            ).order_by(ElectricityReading.year.desc(), ElectricityReading.month.desc()).first()
            if last_reading:
                display_old = last_reading.new_reading

        results.append({
            "room_id": room.id,
            "room_number": room.room_number,
            "rent_fee": bill.rent_fee,
            "service_fee": bill.service_fee,
            "electricity_fee": bill.electricity_fee,
            "old_reading": display_old,
            "new_reading": reading.new_reading if reading else display_old,
            "total": bill.total,
            "status": bill.status,
            "is_occupied": room.is_occupied,
            "paid_at": bill.paid_at,
            "contact_info": bill.tenant_name or room.contact_info,
            "move_in_date": bill.move_in_date or room.move_in_date,
            "deposit": room.deposit,
            "is_fixed": room.electricity_type == "fixed"
        })
            
    return results
            
    return results

@app.post("/api/electricity")
async def update_electricity(data: ElectricityInput, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == data.room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    if room.electricity_type == "fixed":
        return {"message": "Phòng này sử dụng điện khoán"}

    # Lấy giá điện
    unit_price_setting = db.query(Setting).filter(Setting.key == "electricity_unit_price").first()
    unit_price = int(unit_price_setting.value) if unit_price_setting else 4000

    # Tự động tìm số điện cũ (Số điện mới của tháng trước đó gần nhất)
    old_reading = 0
    last_reading = db.query(ElectricityReading).filter(
        ElectricityReading.room_id == data.room_id,
        (ElectricityReading.year < data.year) | 
        ((ElectricityReading.year == data.year) & (ElectricityReading.month < data.month))
    ).order_by(ElectricityReading.year.desc(), ElectricityReading.month.desc()).first()
    
    if last_reading:
        old_reading = last_reading.new_reading

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
    
    # Cập nhật hoặc tạo hóa đơn sau khi nhập điện
    update_bill(db, room, data.month, data.year)
    
    return {"message": "Cập nhật số điện thành công"}

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

@app.post("/api/bills/mark-paid")
async def mark_paid(data: PaidInput, db: Session = Depends(get_db)):
    bill = db.query(MonthlyBill).filter(
        MonthlyBill.room_id == data.room_id,
        MonthlyBill.month == data.month,
        MonthlyBill.year == data.year
    ).first()
    
    if not bill:
        # Nếu chưa có hóa đơn (do chưa nhập điện), tạo mới với số liệu hiện tại
        room = db.query(Room).filter(Room.id == data.room_id).first()
        update_bill(db, room, data.month, data.year)
        bill = db.query(MonthlyBill).filter(
            MonthlyBill.room_id == data.room_id,
            MonthlyBill.month == data.month,
            MonthlyBill.year == data.year
        ).first()

    bill.status = "paid"
    bill.paid_at = datetime.now()
    db.commit()
    return {"message": "Đã đánh dấu thanh toán"}

@app.post("/api/bills/mark-prepaid")
async def mark_prepaid(data: PrepaidInput, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == data.room_id).first()
    if not room: raise HTTPException(status_code=404, detail="Room not found")

    for m in data.months:
        bill = db.query(MonthlyBill).filter(
            MonthlyBill.room_id == data.room_id,
            MonthlyBill.month == m,
            MonthlyBill.year == data.year
        ).first()
        
        if not bill:
            # Đối với trả trước, có thể chưa có số điện, tính theo mặc định
            elec_fee = room.fixed_electricity_fee if room.electricity_type == "fixed" else 0
            bill = MonthlyBill(
                room_id=room.id,
                month=m,
                year=data.year,
                electricity_fee=elec_fee,
                rent_fee=room.rent_price,
                service_fee=room.service_fee,
                total=room.rent_price + room.service_fee + elec_fee,
                status="prepaid",
                prepaid_months=",".join(map(str, data.months)),
                paid_at=datetime.now(),
                tenant_name=room.contact_info,
                move_in_date=room.move_in_date
            )
            db.add(bill)
        else:
            bill.status = "prepaid"
            bill.prepaid_months = ",".join(map(str, data.months))
            bill.paid_at = datetime.now()
            
    db.commit()
    return {"message": "Đã lưu thông tin đóng trước"}

@app.get("/api/rooms/{room_id}/history")
async def get_room_history(room_id: int, db: Session = Depends(get_db)):
    bills = db.query(MonthlyBill).filter(MonthlyBill.room_id == room_id).order_by(MonthlyBill.year.desc(), MonthlyBill.month.desc()).all()
    readings = db.query(ElectricityReading).filter(ElectricityReading.room_id == room_id).all()
    
    # Map readings for easy lookup
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

@app.get("/api/rooms")
async def get_rooms(db: Session = Depends(get_db)):
    return db.query(Room).all()

@app.post("/api/rooms/update")
async def update_room(data: RoomUpdate, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == data.id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # 1. Cập nhật dữ liệu gốc (Master Data) để áp dụng cho tương lai
    room.room_number = data.room_number
    room.rent_price = data.rent_price
    room.service_fee = data.service_fee
    room.deposit = data.deposit
    room.contact_info = data.contact_info
    room.move_in_date = data.move_in_date
    room.electricity_type = data.electricity_type
    room.fixed_electricity_fee = data.fixed_electricity_fee
    # Tự động tính trạng thái đang ở dựa trên tiền phòng và dịch vụ
    room.is_occupied = True if (data.rent_price + data.service_fee > 0) else False
    
    # 2. Nếu có truyền tháng/năm, cập nhật snapshot hóa đơn của tháng đó
    if data.month and data.year:
        # Cập nhật số điện cũ nếu có truyền vào (đặc biệt cho tháng đầu tiên)
        if data.old_reading is not None:
            reading = db.query(ElectricityReading).filter(
                ElectricityReading.room_id == room.id,
                ElectricityReading.month == data.month,
                ElectricityReading.year == data.year
            ).first()
            if reading:
                reading.old_reading = data.old_reading
            else:
                # Tìm giá điện
                unit_price_setting = db.query(Setting).filter(Setting.key == "electricity_unit_price").first()
                unit_price = int(unit_price_setting.value) if unit_price_setting else 4000
                reading = ElectricityReading(
                    room_id=room.id, month=data.month, year=data.year,
                    old_reading=data.old_reading, new_reading=data.old_reading,
                    unit_price=unit_price
                )
                db.add(reading)
            db.flush()

        # Cập nhật hóa đơn
        bill = db.query(MonthlyBill).filter(
            MonthlyBill.room_id == room.id,
            MonthlyBill.month == data.month,
            MonthlyBill.year == data.year
        ).first()
        
        # Tính lại tiền điện dựa trên chỉ số mới nhất
        reading = db.query(ElectricityReading).filter(
            ElectricityReading.room_id == room.id,
            ElectricityReading.month == data.month,
            ElectricityReading.year == data.year
        ).first()
        
        elec_fee = 0
        if room.electricity_type == "fixed":
            elec_fee = room.fixed_electricity_fee
        elif reading:
            elec_fee = max(0, (reading.new_reading - reading.old_reading) * reading.unit_price)

        if bill:
            bill.tenant_name = data.contact_info
            bill.move_in_date = data.move_in_date
            bill.rent_fee = data.rent_price
            bill.service_fee = data.service_fee
            bill.electricity_fee = elec_fee
            bill.total = bill.rent_fee + bill.service_fee + bill.electricity_fee
        else:
            bill = MonthlyBill(
                room_id=room.id,
                month=data.month,
                year=data.year,
                rent_fee=data.rent_price,
                service_fee=data.service_fee,
                electricity_fee=elec_fee,
                total=data.rent_price + data.service_fee + elec_fee,
                status="unpaid",
                tenant_name=data.contact_info,
                move_in_date=data.move_in_date
            )
            db.add(bill)
            
    db.commit()
    return {"message": "Cập nhật thông tin thành công"}

@app.get("/api/settings")
async def get_settings(db: Session = Depends(get_db)):
    settings = db.query(Setting).all()
    return {s.key: s.value for s in settings}

@app.post("/api/settings")
async def update_settings(data: List[SettingUpdate], db: Session = Depends(get_db)):
    for item in data:
        setting = db.query(Setting).filter(Setting.key == item.key).first()
        if setting:
            setting.value = item.value
        else:
            db.add(Setting(key=item.key, value=item.value))
    db.commit()
    return {"message": "Cập nhật cài đặt thành công"}
