from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    # db_url: str = "sqlite+aiosqlite:///./test_db"
    db_url: str = "postgresql+asyncpg://twitter_clone:!1234QWER@db:5432/twitter_clone"
    test_db_url: str = "postgresql+asyncpg://twitter_clone:!1234QWER@db:5432/test_twitter_clone"
    db_echo: bool = True
    base_dir: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    static_dir: str = os.path.join(base_dir, "static")
    dir_uploaded_images: str = os.path.join(static_dir, "tweets_images")


settings = Settings()
