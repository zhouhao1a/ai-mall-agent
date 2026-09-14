from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# 项目根目录：app/core/config.py 往上数三层
BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",  # ← 改成绝对路径
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str
    redis_url: str
    app_env: str = "dev"
    log_level: str = "DEBUG"
    jwt_secret: str
    jwt_expire_minutes: int = 30


settings = Settings()