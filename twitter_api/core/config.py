from dotenv import load_dotenv

import os

from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DB_USERNAME: str = os.environ.get('DB_USERNAME')
    DB_PASSWORD: str = os.environ.get('DB_PASSWORD')
    DB_HOST: str = os.environ.get('DB_HOST')
    DB_TEST_HOST: str = os.environ.get('TEST_DB_HOST')
    DB_PORT: str = os.environ.get('DB_PORT')
    DB_NAME: str = os.environ.get("DB_NAME")
    TEST_DB_NAME: str = os.environ.get("TEST_DB_NAME")

    db_url: str = (
        f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    test_db_url: str = (
        f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_TEST_HOST}:{DB_PORT}/{TEST_DB_NAME}"
    )
    db_echo: bool = True
    base_dir: str = os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__),
            ),
        ),
    )
    static_dir: str = os.path.join(
        base_dir,
        "static",
    )
    dir_uploaded_images: str = os.path.join(
        static_dir,
        "tweets_images",
    )


settings = Settings()
