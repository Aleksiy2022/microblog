from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "postgresql+asyncpg://twitter_clone:!1234QWER@db:5432/twitter_clone"
    # db_url: str = "sqlite+aiosqlite:///./twitter_clone_db"
    db_echo: bool = True


settings = Settings()
