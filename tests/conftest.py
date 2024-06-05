import os
from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

from api.core import settings, test_db_helper
from api.db import Base
from api.dependencies import get_current_user_by_api_key, scoped_session_db
from api.main import app

from .factories import create_test_data_bd
from .overrides_dependencies import (
    ovr_get_current_user_by_api_key,
    ovr_scoped_session_db,
)

DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_TEST_HOST = os.environ.get("TEST_DB_HOST")
TEST_DB_NAME = os.environ.get("TEST_DB_NAME")
DB_PORT = os.environ.get("DB_PORT")
test_dir = os.path.dirname(__file__)


app.dependency_overrides[scoped_session_db] = ovr_scoped_session_db
app.dependency_overrides[get_current_user_by_api_key] = (
    ovr_get_current_user_by_api_key
)


@pytest.fixture(autouse=True, scope="session")
async def set_test_settings():
    test_dir_uploaded_images = os.path.join(
        test_dir, "test_api",
        "test_routers", "uploaded_test_images"
    )
    settings.dir_uploaded_images = test_dir_uploaded_images
    yield
    file_path = os.path.join(test_dir_uploaded_images, "light_image.jpg")
    os.remove(file_path)


@pytest.fixture(autouse=True, scope="session")
async def create_test_db():
    async with test_db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await create_test_data_bd()
    yield

    async with test_db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(autouse=True, scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"  # type: ignore
    ) as async_client:
        yield async_client
