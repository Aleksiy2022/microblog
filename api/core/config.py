import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """
    Settings class that holds configuration for the project.

    Attributes:
        db_username (str | None): Username for the database,
        fetched from env variable 'DB_USERNAME'.
        db_password (str | None): Password for the database,
        fetched from env variable 'DB_PASSWORD'.
        db_host (str | None): Host for the database,
        fetched from envi variable 'DB_HOST'.
        db_test_host (str | None): Host for the test database,
        fetched from envi variable 'TEST_DB_HOST'.
        db_port (str | None): Port for the database,
        fetched from envi variable 'DB_PORT'.
        db_name (str | None): Name of the database,
        fetched from envi variable 'DB_NAME'.
        test_db_name (str | None): Name of the test database,
        fetched from envi variable 'TEST_DB_NAME'.
        max_file_size_bytes (int): Maximum file size for uploads. Defaults to 1048576 bytes (1 MB).
        db_url (str): Constructed URL for connecting to the database using asyncpg.
        test_db_url (str): Constructed URL for connecting to the test database using asyncpg.
        db_echo (bool): Enables SQLAlchemy logging. Defaults to True.
        base_dir (str): Base directory path of the project.
        static_dir (str): Directory path for static files.
        dir_uploaded_images (str): Directory path for uploaded image files.
    """

    db_username: str | None = os.environ.get("DB_USERNAME")
    db_password: str | None = os.environ.get("DB_PASSWORD")
    db_host: str | None = os.environ.get("DB_HOST")
    db_name: str | None = os.environ.get("DB_NAME")
    test_db_name: str | None = os.environ.get("TEST_DB_NAME")
    max_file_size_bytes: int = 1048576
    db_url: str = (
        f"postgresql+asyncpg://{db_username}:{db_password}@db:5432/{db_name}"
    )
    test_db_url: str = (
        f"postgresql+asyncpg://{db_username}:{db_password}@localhost:5432/{test_db_name}"
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
