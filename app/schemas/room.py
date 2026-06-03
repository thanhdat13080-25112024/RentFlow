from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


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
    id: int = Field(ge=1)
    room_number: str = Field(min_length=1)
    rent_price: int = Field(ge=0)
    service_fee: int = Field(ge=0)
    deposit: int = Field(ge=0)
    contact_info: Optional[str] = None
    move_in_date: Optional[str] = None
    electricity_type: Literal["meter", "fixed"]
    fixed_electricity_fee: int = Field(ge=0)
    is_occupied: bool
    month: Optional[int] = Field(default=None, ge=1, le=12)
    year: Optional[int] = Field(default=None, ge=2000, le=2100)
    old_reading: Optional[int] = Field(default=None, ge=0)


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
