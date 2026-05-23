from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db import Base


class ElectricityReading(Base):
    __tablename__ = "electricity_readings"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    month = Column(Integer)
    year = Column(Integer)
    old_reading = Column(Integer)
    new_reading = Column(Integer)
    unit_price = Column(Integer)

    room = relationship("Room", back_populates="readings")
