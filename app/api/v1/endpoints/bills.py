import csv
import io
from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models import ElectricityReading, MonthlyBill, Room
from app.schemas import BillPaidUpdate, BillPrepaidUpdate
from app.services.billing import compute_bill_fields, get_unit_price, update_bill

router = APIRouter()

@router.get("/revenue/summary")
async def get_revenue_summary(db: Session = Depends(get_db)):
    # Chỉ ĐỌC: tính doanh thu ảo (không ghi DB) cho các phòng ĐANG THUÊ.
    # Dùng giá trị bill đã lưu nếu có, ngược lại tính từ số điện — cho ra cùng
    # con số như trước nhưng không tạo hàng trăm bill / commit mỗi lần mở dashboard,
    # và không cộng doanh thu ảo của phòng trống.
    bill_periods = db.query(MonthlyBill.month, MonthlyBill.year).distinct().all()
    reading_periods = db.query(ElectricityReading.month, ElectricityReading.year).distinct().all()

    all_periods = set(bill_periods) | set(reading_periods)
    now = datetime.now()
    all_periods.add((now.month, now.year))

    rooms = db.query(Room).filter(Room.is_occupied == True).all()  # noqa: E712 (B2)
    bill_map = {(b.room_id, b.month, b.year): b for b in db.query(MonthlyBill).all()}
    reading_map = {(r.room_id, r.month, r.year): r for r in db.query(ElectricityReading).all()}

    results = []
    for m, y in sorted(all_periods, key=lambda p: (p[1], p[0]), reverse=True):
        agg = {"total_elec": 0, "total_service": 0, "total_rent": 0, "total_revenue": 0}
        for room in rooms:
            bill = bill_map.get((room.id, m, y))
            if bill:
                elec, serv, rent, tot = bill.electricity_fee, bill.service_fee, bill.rent_fee, bill.total
            else:
                f = compute_bill_fields(room, reading_map.get((room.id, m, y)))
                elec, serv, rent, tot = f["electricity_fee"], f["service_fee"], f["rent_fee"], f["total"]
            agg["total_elec"] += elec or 0
            agg["total_service"] += serv or 0
            agg["total_rent"] += rent or 0
            agg["total_revenue"] += tot or 0
        results.append({"year": y, "month": m, **agg})

    return results

def _collect_bills(db: Session, month: int, year: int):
    # Chỉ ĐỌC: dùng bill đã lưu nếu có, ngược lại tính ảo (không ghi DB).
    # Bill được tạo/ghi ở các luồng GHI (nhập điện, thu tiền, sửa phòng), không ở đây.
    # Dùng chung cho GET /api/bills/ và GET /api/bills/export.
    rooms = db.query(Room).all()
    results = []

    for room in rooms:
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

        if bill:
            rent_fee, service_fee = bill.rent_fee, bill.service_fee
            electricity_fee, total, status = bill.electricity_fee, bill.total, bill.status
            paid_at = bill.paid_at
            contact_info = bill.tenant_name or room.contact_info
            move_in_date = bill.move_in_date or room.move_in_date
        else:
            f = compute_bill_fields(room, reading)
            rent_fee, service_fee = f["rent_fee"], f["service_fee"]
            electricity_fee, total, status = f["electricity_fee"], f["total"], "unpaid"
            paid_at = None
            contact_info = room.contact_info
            move_in_date = room.move_in_date

        results.append({
            "room_id": room.id,
            "room_number": room.room_number,
            "rent_fee": rent_fee,
            "service_fee": service_fee,
            "electricity_fee": electricity_fee,
            "old_reading": display_old,
            "new_reading": reading.new_reading if reading else display_old,
            "total": total,
            "status": status,
            "is_occupied": room.is_occupied,
            "paid_at": paid_at,
            "contact_info": contact_info,
            "move_in_date": move_in_date,
            "deposit": room.deposit,
            "is_fixed": room.electricity_type == "fixed"
        })

    return results


@router.get("/")
async def get_bills(month: int, year: int, db: Session = Depends(get_db)):
    return _collect_bills(db, month, year)


@router.get("/receivables")
async def get_receivables(db: Session = Depends(get_db)):
    """Công nợ: tổng tiền các hoá đơn CHƯA THU của phòng đang thuê, gộp theo phòng.

    Chỉ tính bill đã ghi (status='unpaid') — bill được ghi khi nhập điện / sửa phòng,
    nên phản ánh các tháng đã phát sinh nhưng chưa thu."""
    occupied = {r.id: r for r in db.query(Room).filter(Room.is_occupied == True).all()}  # noqa: E712
    if not occupied:
        return {"total": 0, "count": 0, "rooms": []}

    unpaid = db.query(MonthlyBill).filter(
        MonthlyBill.status == "unpaid",
        MonthlyBill.room_id.in_(list(occupied.keys())),
    ).all()

    by_room = {}
    for b in unpaid:
        e = by_room.setdefault(b.room_id, {"amount": 0, "months": 0})
        e["amount"] += b.total or 0
        e["months"] += 1

    rooms = [
        {
            "room_id": rid,
            "room_number": occupied[rid].room_number,
            "tenant_name": occupied[rid].contact_info,
            "months": e["months"],
            "amount": e["amount"],
        }
        for rid, e in by_room.items()
    ]
    rooms.sort(key=lambda x: x["amount"], reverse=True)
    return {"total": sum(x["amount"] for x in rooms), "count": len(rooms), "rooms": rooms}


@router.get("/export")
async def export_bills(month: int, year: int, db: Session = Depends(get_db)):
    """Xuất hoá đơn của 1 tháng ra CSV (định dạng tương thích với import-csv)."""
    status_vi = {"unpaid": "Chưa thu", "paid": "Đã thu", "prepaid": "Đóng trước"}
    out = io.StringIO()
    out.write("﻿")  # BOM để Excel mở đúng tiếng Việt
    writer = csv.writer(out)
    writer.writerow([
        "Phòng", "Khách Thuê", "Tháng", "Năm", "Tiền Phòng", "Dịch Vụ",
        "Điện Cũ", "Điện Mới", "Tiền Điện", "Tổng", "Trạng Thái",
    ])
    for r in _collect_bills(db, month, year):
        if not r["is_occupied"]:
            continue
        writer.writerow([
            r["room_number"], r.get("contact_info") or "", month, year,
            r["rent_fee"], r["service_fee"], r["old_reading"], r["new_reading"],
            r["electricity_fee"], r["total"], status_vi.get(r["status"], r["status"]),
        ])
    return Response(
        content=out.getvalue(),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="hoadon_{month}_{year}.csv"'},
    )

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
        
        unit_price = get_unit_price(db)

        def get_val(row, keys, default=None):
            for k in keys:
                if k in row: return row[k]
            return default

        import_count = 0
        error_count = 0
        for row in reader:
            try:
                room_number = get_val(row, ["Phòng", "Phong", "Room", "room"])
                month_val = get_val(row, ["Tháng", "Thang", "Month", "month"])
                year_val = get_val(row, ["Năm", "Nam", "Year", "year"])

                if not room_number or not month_val or not year_val:
                    continue

                month = int(month_val)
                year = int(year_val)

                room = db.query(Room).filter(Room.room_number == room_number).first()
                if not room:
                    continue

                room.contact_info = get_val(row, ["Khách Thuê", "Khach Thue", "Tenant", "tenant"], room.contact_info)
                room.move_in_date = get_val(row, ["Ngày Vào", "Ngay Vao", "Move In", "date"], room.move_in_date)

                rent_val = get_val(row, ["Tiền Phòng", "Tien Phong", "Rent", "rent"])
                if rent_val is not None: room.rent_price = int(rent_val)

                service_val = get_val(row, ["Dịch Vụ", "Dich Vu", "Service", "service"])
                if service_val is not None: room.service_fee = int(service_val)

                room.is_occupied = bool(room.contact_info and str(room.contact_info).strip())

                old_r = get_val(row, ["Điện Cũ", "Dien Cu", "Old Reading", "old"])
                new_r = get_val(row, ["Điện Mới", "Dien Moi", "New Reading", "new"])
                elec_fee = 0

                if old_r is not None and new_r is not None and str(old_r).strip() != "" and str(new_r).strip() != "":
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

                status_map = {
                    "Da thu": "paid", "Đã thu": "paid", "Paid": "paid",
                    "Chua thu": "unpaid", "Chưa thu": "unpaid", "Unpaid": "unpaid",
                    "Dong truoc": "prepaid", "Đóng trước": "prepaid", "Prepaid": "prepaid"
                }
                raw_status = get_val(row, ["Trạng Thái", "Trang Thai", "Status", "status"], "Chua thu")
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
            except Exception:
                # Một dòng lỗi (dữ liệu bẩn) không làm hỏng cả lần import.
                error_count += 1
                continue

        db.commit()
        msg = f"Đã import thành công {import_count} dòng dữ liệu"
        if error_count:
            msg += f" ({error_count} dòng lỗi bị bỏ qua)"
        return {"message": msg}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
