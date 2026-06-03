from datetime import datetime
from typing import Annotated, List, Optional

from pydantic import BaseModel, Field


class BillPaidUpdate(BaseModel):
    room_id: int = Field(ge=1)
    month: int = Field(ge=1, le=12)
    year: int = Field(ge=2000, le=2100)


class BillPrepaidUpdate(BaseModel):
    room_id: int = Field(ge=1)
    months: List[Annotated[int, Field(ge=1, le=12)]] = Field(min_length=1)
    year: int = Field(ge=2000, le=2100)


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
