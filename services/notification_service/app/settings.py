from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    cors_origins: list[str] = ["*"]
    app_name: str = "Country GraphQL Notification Service"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
