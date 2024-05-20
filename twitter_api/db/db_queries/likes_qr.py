from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import TweetLike


async def create_tweet_like(
    session: AsyncSession,
    tweet_id: int,
    current_user_id: int,
) -> bool:
    new_tweet_like = TweetLike(
        tweet_id=tweet_id,
        user_id=current_user_id,
    )
    session.add(new_tweet_like)
    await session.commit()
    return True


async def delete_tweet_like(
    session: AsyncSession, tweet_id: int, current_user_id: int
) -> bool:
    stmt = delete(TweetLike).where(
        TweetLike.tweet_id == tweet_id,
        TweetLike.user_id == current_user_id,
    )
    await session.execute(stmt)
    await session.commit()
    return True
