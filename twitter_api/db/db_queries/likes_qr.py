from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from ..models import TweetLike, User
from .users_qr import get_current_user_id


async def create_tweet_like(session: AsyncSession, tweet_id: int, api_key: str) -> bool:
    user_id = await get_current_user_id(session, api_key=api_key)
    new_tweet_like = TweetLike(
        tweet_id=tweet_id,
        user_id=user_id
    )
    session.add(new_tweet_like)
    await session.commit()
    return True


async def delete_tweet_like(session: AsyncSession, tweet_id: int, api_key: str) -> bool:
    user_id = await get_current_user_id(session, api_key=api_key)
    stmt = delete(TweetLike).where(TweetLike.tweet_id == tweet_id, User.id == user_id)
    await session.execute(stmt)
    await session.commit()
    return True
