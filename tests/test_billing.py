"""Unit tests for the core billing logic (app/services/billing.py)."""
from app.models import ElectricityReading, MonthlyBill, Room
from app.services.billing import compute_bill_fields, update_bill


def _room(**kw):
    defaults = dict(
        room_number="101", rent_price=2000000, service_fee=100000, deposit=0,
        contact_info="Khách A", move_in_date=None, electricity_type="meter",
        fixed_electricity_fee=0, is_occupied=True,
    )
    defaults.update(kw)
    return Room(**defaults)


# ── compute_bill_fields: pure, no DB ──

def test_compute_meter_with_reading():
    room = _room(electricity_type="meter", rent_price=2000000, service_fee=100000)
    reading = ElectricityReading(old_reading=100, new_reading=150, unit_price=4000)
    f = compute_bill_fields(room, reading)
    assert f["electricity_fee"] == 200000          # (150-100) * 4000
    assert f["total"] == 2000000 + 100000 + 200000


def test_compute_meter_without_reading_is_zero_elec():
    f = compute_bill_fields(_room(electricity_type="meter"), None)
    assert f["electricity_fee"] == 0
    assert f["total"] == 2000000 + 100000


def test_compute_fixed_ignores_reading():
    room = _room(electricity_type="fixed", fixed_electricity_fee=150000)
    # Even with a huge reading, fixed rooms use the flat fee.
    reading = ElectricityReading(old_reading=0, new_reading=9999, unit_price=4000)
    f = compute_bill_fields(room, reading)
    assert f["electricity_fee"] == 150000


# ── update_bill: writes, with the "don't overwrite paid" rule ──

def test_update_bill_creates_unpaid(db):
    room = _room()
    db.add(room)
    db.commit()
    update_bill(db, room, 6, 2026)
    bill = db.query(MonthlyBill).filter_by(room_id=room.id, month=6, year=2026).first()
    assert bill is not None
    assert bill.status == "unpaid"
    assert bill.total == room.rent_price + room.service_fee


def test_update_bill_refreshes_unpaid(db):
    room = _room(rent_price=2000000)
    db.add(room)
    db.commit()
    update_bill(db, room, 6, 2026)
    room.rent_price = 3000000
    db.commit()
    update_bill(db, room, 6, 2026)
    bill = db.query(MonthlyBill).filter_by(room_id=room.id).first()
    assert bill.total == 3000000 + 100000  # unpaid bill is recalculated


def test_update_bill_never_overwrites_paid(db):
    room = _room()
    db.add(room)
    db.commit()
    update_bill(db, room, 6, 2026)
    bill = db.query(MonthlyBill).filter_by(room_id=room.id).first()
    bill.status = "paid"
    bill.total = 12345
    db.commit()
    # Changing the room afterwards must NOT alter a paid bill.
    room.rent_price = 9000000
    db.commit()
    update_bill(db, room, 6, 2026)
    db.refresh(bill)
    assert bill.status == "paid"
    assert bill.total == 12345
