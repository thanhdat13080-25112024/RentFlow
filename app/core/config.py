from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Quản Lý Trọ"
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./rentflow.db"
    
    # Electricity settings
    DEFAULT_ELECTRICITY_UNIT_PRICE: int = 4000
    
    # Bank settings
    BANK_NAME: str = "MB"
    BANK_ACCOUNT: str = ""
    ACCOUNT_HOLDER: str = ""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
