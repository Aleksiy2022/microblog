from sqlalchemy.ext.asyncio import AsyncSession
from ..models import User, Follower
from sqlalchemy import select, delete
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


async def create_user_following_node(session: AsyncSession, follower_id: int = None, user_id: int = None) -> bool:
    new_user_following_node = Follower(
        user_id=user_id,
        follower=follower_id,
    )
    session.add(new_user_following_node)
    await session.commit()
    return True


async def delete_user_following_node(session: AsyncSession, follower_id: int = None, user_id: int = None) -> bool:
    stmt = delete(Follower).where(Follower.user_id == user_id, Follower.follower == follower_id)
    await session.execute(stmt)
    await session.commit()
    return True
