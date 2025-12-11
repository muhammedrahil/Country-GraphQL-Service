from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    database_url: Optional[str] = None
    cors_origins: list[str] = ["*"]
    app_name: str = "Country GraphQL Service"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
