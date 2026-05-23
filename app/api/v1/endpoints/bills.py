from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime
import io
import csv
from app.db import get_db
from app.models import ElectricityReading, MonthlyBill, Room, Setting
from app.schemas.data_transfer_objects import BillPaidUpdate, BillPrepaidUpdate
from app.services.billing import update_bill

router = APIRouter()

@router.get("/revenue/summary")
async def get_revenue_summary(db: Session = Depends(get_db)):
    bill_periods = db.query(MonthlyBill.month, MonthlyBill.year).distinct().all()
    reading_periods = db.query(ElectricityReading.month, ElectricityReading.year).distinct().all()
    
    all_periods = set(bill_periods) | set(reading_periods)
    
    now = datetime.now()
    all_periods.add((now.month, now.year))
    # Removed hardcoded (4, 2026)

    rooms = db.query(Room).all()
    for m, y in all_periods:
        for room in rooms:
            update_bill(db, room, m, y)

    results = db.query(
        MonthlyBill.year,
        MonthlyBill.month,
        func.sum(MonthlyBill.electricity_fee).label("total_elec"),
        func.sum(MonthlyBill.service_fee).label("total_service"),
        func.sum(MonthlyBill.rent_fee).label("total_rent"),
        func.sum(MonthlyBill.total).label("total_revenue")
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

@router.get("/")
async def get_bills(month: int, year: int, db: Session = Depends(get_db)):
    rooms = db.query(Room).all()
    results = []
    
    for room in rooms:
        update_bill(db, room, month, year)
        
        bill = db.query(MonthlyBill).filter(
            MonthlyBill.room_id == room.id,
            MonthlyBill.month == month,
            MonthlyBill.year == year
        ).first()
        
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

@router.post("/mark-paid")
async def mark_paid(data: BillPaidUpdate, db: Session = Depends(get_db)):
    bill = db.query(MonthlyBill).filter(
        MonthlyBill.room_id == data.room_id,
        MonthlyBill.month == data.month,
        MonthlyBill.year == data.year
    ).first()
    
    if not bill:
        room = db.query(Room).filter(Room.id == data.room_id).first()
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        update_bill(db, room, data.month, data.year)
        bill = db.query(MonthlyBill).filter(
            MonthlyBill.room_id == data.room_id,
            MonthlyBill.month == data.month,
            MonthlyBill.year == data.year
        ).first()

    if not bill:
        raise HTTPException(status_code=404, detail="Bill could not be created")

    bill.status = "paid"
    bill.paid_at = datetime.now()
    db.commit()
    return {"message": "Đã đánh dấu thanh toán"}

@router.post("/mark-prepaid")
async def mark_prepaid(data: BillPrepaidUpdate, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == data.room_id).first()
    if not room: raise HTTPException(status_code=404, detail="Room not found")

    for m in data.months:
        bill = db.query(MonthlyBill).filter(
            MonthlyBill.room_id == data.room_id,
            MonthlyBill.month == m,
            MonthlyBill.year == data.year
        ).first()
        
        if not bill:
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

@router.post("/import-csv")
async def import_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        content = await file.read()
        stream = io.StringIO(content.decode("utf-8-sig"))
        reader = csv.DictReader(stream)
        
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

            room.contact_info = row.get("Khách Thuê", room.contact_info)
            room.move_in_date = row.get("Ngày Vào", room.move_in_date)
            room.rent_price = int(row.get("Tiền Phòng", room.rent_price))
            room.service_fee = int(row.get("Dịch Vụ", room.service_fee))
            room.is_occupied = True if (room.rent_price + room.service_fee > 0) else False
            
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
