from pydantic import BaseModel


class ElectricityReadingCreate(BaseModel):
    room_id: int
    month: int
    year: int
    new_reading: int
