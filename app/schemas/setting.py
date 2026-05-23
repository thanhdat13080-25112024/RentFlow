from pydantic import BaseModel


class SettingUpdate(BaseModel):
    key: str
    value: str


class SettingRead(BaseModel):
    key: str
    value: str
