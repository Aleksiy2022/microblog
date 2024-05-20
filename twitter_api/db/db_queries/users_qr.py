from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from ..models import Follower, User


async def get_current_user(
    session: AsyncSession,
    api_key: str,
) -> User:
    stmt = select(User).where(User.api_key == api_key)
    user: User | None = await session.scalar(stmt)
    if user:
        return user
    else:
        raise ValueError(f"API key {api_key} does not match")


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    stmt = (
        select(User)
        .options(
            joinedload(User.followers),
            joinedload(User.following),
        )
        .where(User.id == user_id)
    )
    user: User | None = await session.scalar(stmt)
    return user if user else None


async def create_user_following_node(
    session: AsyncSession,
    follower_id: int,
    user_id: int,
) -> bool:
    new_user_following_node = Follower(
        user_id=user_id,
        follower=follower_id,
    )
    session.add(new_user_following_node)
    await session.commit()
    return True


async def delete_user_following_node(
    session: AsyncSession,
    follower_id: int,
    user_id: int,
) -> bool:
    stmt = delete(Follower).where(
        Follower.user_id == user_id,
        Follower.follower == follower_id,
    )
    await session.execute(stmt)
    await session.commit()
    return True
