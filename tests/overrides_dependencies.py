from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, AsyncGenerator
from sqlalchemy import select
from twitter_api.db import User
from twitter_api.core import test_db_helper
from fastapi import Header, Depends, HTTPException


async def ovr_scoped_session_db() -> AsyncGenerator[AsyncSession, None]:
    session = test_db_helper.get_scoped_session()
    yield session
    await session.close()


async def ovr_get_current_user_by_api_key(
    session: Annotated[AsyncSession, Depends(ovr_scoped_session_db)],
    api_key: Annotated[str, Header(max_length=30)],
) -> User:
    stmt = select(User).where(User.api_key == api_key)
    user = await session.scalar(stmt)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with api_key: {api_key} not found"
        )
    return user
