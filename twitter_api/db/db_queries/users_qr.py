from sqlalchemy.ext.asyncio import AsyncSession
from ..models import User
from sqlalchemy import select
from sqlalchemy.orm import joinedload


async def get_current_user_id(session: AsyncSession, api_key: str) -> int:
    stmt = select(User).where(User.api_key == api_key)
    user = await session.scalar(stmt)
    return user.id


async def get_user_by_api_key(session: AsyncSession, api_key: str = None) -> User:
    stmt = (
        select(User).
        options(
            joinedload(User.followers),
            joinedload(User.following)
        ).
        where(User.api_key == api_key)
    )
    user: User | None = await session.scalar(stmt)
    return user


async def get_user_by_id(session: AsyncSession, user_id: int) -> User:
    stmt = (
        select(User).
        options(
            joinedload(User.followers),
            joinedload(User.following)
        ).
        where(User.id == user_id)
    )
    user: User | None = await session.scalar(stmt)
    return user
