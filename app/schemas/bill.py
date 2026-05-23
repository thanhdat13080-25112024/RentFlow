from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class BillPaidUpdate(BaseModel):
    room_id: int
    month: int
    year: int


class BillPrepaidUpdate(BaseModel):
    room_id: int
    months: List[int]
    year: int


class BillRead(BaseModel):
    room_id: int
    room_number: str
    rent_fee: int
    service_fee: int
    electricity_fee: int
    old_reading: int
    new_reading: int
    total: int
    status: str
    is_occupied: bool
    paid_at: Optional[datetime]
    contact_info: Optional[str]
    move_in_date: Optional[str]
    deposit: int
    is_fixed: bool


class RevenueSummaryRead(BaseModel):
    year: int
    month: int
    total_elec: int
    total_service: int
    total_rent: int
    total_revenue: int
