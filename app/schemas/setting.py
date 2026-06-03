from pydantic import BaseModel, Field


class SettingUpdate(BaseModel):
    key: str = Field(min_length=1)
    value: str


class SettingRead(BaseModel):
    key: str
    value: str
