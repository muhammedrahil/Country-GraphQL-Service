from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    database_url: Optional[str] = None
    cors_origins: list[str] = ["*"]
    app_name: str = "Country GraphQL Service"
    notification_service: str = "http://localhost:8001"
    ingestion_api_url: str = "https://www.apicountries.com/countries"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
