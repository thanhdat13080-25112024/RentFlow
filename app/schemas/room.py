from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class RoomRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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


class RoomHistoryRead(BaseModel):
    month: int
    year: int
    tenant_name: Optional[str]
    rent_fee: int
    service_fee: int
    electricity_fee: int
    total: int
    status: str
    paid_at: Optional[datetime]
    old_reading: int
    new_reading: int
    usage: int
