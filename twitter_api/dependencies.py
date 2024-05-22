from typing import Annotated, AsyncGenerator

from fastapi import Depends, Header
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .core import db_helper
from .db import User, users_qr


async def scoped_session_db() -> AsyncGenerator[AsyncSession, None]:
    session = db_helper.get_scoped_session()
    yield session
    await session.close()


async def get_current_user_by_api_key(
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
    api_key: Annotated[str, Header(max_length=30)],
) -> User:
    user = await users_qr.get_current_user(session, api_key=api_key)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with api_key: {api_key} not found"
        )
    return user
