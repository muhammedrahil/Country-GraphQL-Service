from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    database_url: str = (
        "postgresql+asyncpg://postgres:Zaigo%4025@localhost:5433/country-graphql-service"
    )
    cors_origins: list[str] = ["*"]
    app_name: str = "Country GraphQL Service"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
