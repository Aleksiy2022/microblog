from httpx import AsyncClient, ASGITransport
from twitter_api.core import test_db_helper
from typing import AsyncGenerator
from twitter_api.main import app
from twitter_api.dependencies import scoped_session_db, get_current_user_by_api_key
import pytest
from twitter_api.db import Base
from .factories import create_test_data_bd
from .overrides_dependencies import ovr_scoped_session_db, ovr_get_current_user_by_api_key


app.dependency_overrides[scoped_session_db] = ovr_scoped_session_db
app.dependency_overrides[get_current_user_by_api_key] = ovr_get_current_user_by_api_key


@pytest.fixture(autouse=True, scope='session')
async def create_test_db():
    async with test_db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    async with test_db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await create_test_data_bd()

    yield
    async with test_db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(autouse=True, scope='session')
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as async_client:
        yield async_client
