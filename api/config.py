from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # db_url: str = "postgresql+asyncpg://admin:!1234QWER@db:5432/twitter_clone"
    db_url: str = "sqlite+aiosqlite:///api_bd"
    db_echo: bool = True


settings = Settings()
