import secrets
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_ENV_FILE = Path(".env")

def _get_or_create_secret_key() -> str:
    """Đọc SECRET_KEY từ .env; nếu chưa có thì sinh mới và ghi vào .env
    để các lần restart sau dùng lại key, tránh invalidate JWT token."""
    if _ENV_FILE.exists():
        for line in _ENV_FILE.read_text(encoding="utf-8").splitlines():
            if line.startswith("SECRET_KEY="):
                return line.split("=", 1)[1].strip()
    key = secrets.token_urlsafe(32)
    with _ENV_FILE.open("a", encoding="utf-8") as f:
        f.write(f"\nSECRET_KEY={key}\n")
    return key

class Settings(BaseSettings):
    PROJECT_NAME: str = "RentFlow"
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./rentflow.db"

    # Môi trường chạy: "development" (mặc định) hoặc "production".
    # production → cookie auth bật secure=True (yêu cầu HTTPS).
    ENVIRONMENT: str = "development"

    # Server settings
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # Auth settings
    SECRET_KEY: str = _get_or_create_secret_key()
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Admin credentials
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin123" # Khuyên dùng đổi qua .env

    # Electricity settings — giá điện mặc định khi bảng settings chưa có
    # (seeder cũng dùng đúng giá trị này để đồng bộ một nguồn duy nhất).
    DEFAULT_ELECTRICITY_UNIT_PRICE: int = 3500

    # Bank settings
    BANK_NAME: str = "MB"
    BANK_ACCOUNT: str = ""
    ACCOUNT_HOLDER: str = ""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
