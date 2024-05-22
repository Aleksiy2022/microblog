from sqlalchemy import delete, select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
from ..models import Follower, User


async def get_current_user(
    session: AsyncSession,
    api_key: str,
) -> User | None:
    stmt = select(User).where(User.api_key == api_key)
    user: User | None = await session.scalar(stmt)
    return user if user else None


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
    stmt = select(exists().where(User.id == user_id))
    user = await session.scalar(stmt)
    if user:
        stmt = select(exists().where(Follower.user_id == user_id, Follower.follower == follower_id))
        user_follower_node = await session.scalar(stmt)
        if not user_follower_node:
            new_user_following_node = Follower(
                user_id=user_id,
                follower=follower_id,
            )
            session.add(new_user_following_node)
            await session.commit()
            return True
        else:
            raise HTTPException(status_code=409, detail=f"You have already subscribed to this user with id: {user_id}")
    else:
        raise HTTPException(status_code=404, detail=f"User with id: {user_id} not found")


async def delete_user_following_node(
    session: AsyncSession,
    follower_id: int,
    user_id: int,
) -> bool:
    stmt = select(exists().where(Follower.user_id == user_id, Follower.follower == follower_id))
    user_following_node = await session.scalar(stmt)
    if user_following_node:
        stmt = delete(Follower).where(
            Follower.user_id == user_id,
            Follower.follower == follower_id,
        )
        await session.execute(stmt)
        await session.commit()
        return True
    else:
        raise HTTPException(status_code=404, detail=f"You are not subscribed to a user with id {user_id}")
