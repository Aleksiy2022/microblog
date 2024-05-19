from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from .core import db_helper
from fastapi import Header
from typing import Annotated


async def scoped_session_db() -> AsyncGenerator[AsyncSession, None]:
    session = db_helper.get_scoped_session()
    yield session
    await session.close()


async def get_api_key(api_key: Annotated[str | None, Header()]):
    return api_key
