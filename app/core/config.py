from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import secrets

class Settings(BaseSettings):
    PROJECT_NAME: str = "RentFlow"
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./rentflow.db"
    
    # Auth settings
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Admin credentials
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin123" # Khuyên dùng đổi qua .env
    
    # Electricity settings
    DEFAULT_ELECTRICITY_UNIT_PRICE: int = 4000
    
    # Bank settings
    BANK_NAME: str = "MB"
    BANK_ACCOUNT: str = ""
    ACCOUNT_HOLDER: str = ""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
