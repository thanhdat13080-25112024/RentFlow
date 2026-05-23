from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.models import Setting
from app.schemas.data_transfer_objects import SettingUpdate

router = APIRouter()

@router.get("/")
async def get_settings(db: Session = Depends(get_db)):
    settings = db.query(Setting).all()
    return {s.key: s.value for s in settings}

@router.post("/")
async def update_settings(data: List[SettingUpdate], db: Session = Depends(get_db)):
    for item in data:
        setting = db.query(Setting).filter(Setting.key == item.key).first()
        if setting:
            setting.value = item.value
        else:
            db.add(Setting(key=item.key, value=item.value))
    db.commit()
    return {"message": "Cập nhật cài đặt thành công"}
