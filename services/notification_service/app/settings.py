from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    smtp_host: Optional[str] = None
    smtp_port: Optional[str] = None
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    from_email: Optional[str] = None
    admin_email: Optional[str] = None
    cors_origins: list[str] = ["*"]
    app_name: str = "Country GraphQL Notification Service"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
