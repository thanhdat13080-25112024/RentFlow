from pydantic import BaseModel, Field


class ElectricityReadingCreate(BaseModel):
    room_id: int = Field(ge=1)
    month: int = Field(ge=1, le=12)
    year: int = Field(ge=2000, le=2100)
    new_reading: int = Field(ge=0)
