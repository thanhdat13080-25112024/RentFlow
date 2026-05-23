from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

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

class SettingResponse(BaseModel):
    key: str
    value: str

class RoomResponse(BaseModel):
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

class RevenueSummaryResponse(BaseModel):
    year: int
    month: int
    total_elec: int
    total_service: int
    total_rent: int
    total_revenue: int

class BillResponse(BaseModel):
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

class RoomHistoryResponse(BaseModel):
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
