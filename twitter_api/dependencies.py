from typing import Annotated, AsyncGenerator

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from .core import db_helper
from .db import User, users_qr


async def scoped_session_db() -> AsyncGenerator[AsyncSession, None]:
    session = db_helper.get_scoped_session()
    yield session
    await session.close()


async def get_current_user_by_api_key(
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
    api_key: Annotated[str, Header()],
) -> User:
    return await users_qr.get_current_user(session, api_key=api_key)
