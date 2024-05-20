from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models import Image, Tweet


async def get_all_tweets(session: AsyncSession) -> list[Tweet]:
    stmt = select(Tweet).options(
        selectinload(Tweet.author),
        selectinload(Tweet.tweet_likes),
        selectinload(Tweet.attachments).load_only(Image.src),
    )
    tweets = await session.scalars(stmt)
    return list(tweets)


async def create_tweet(
    session: AsyncSession,
    content: str,
    current_user_id: int,
) -> int:
    tweet = Tweet(
        content=content,
        user_id=current_user_id,
    )
    session.add(tweet)
    await session.commit()
    await session.refresh(tweet)
    return tweet.id


async def delete_tweet(
    session: AsyncSession,
    tweet_id: int,
    current_user_id: int,
) -> bool:
    stmt = delete(Tweet).where(
        Tweet.id == tweet_id,
        Tweet.user_id == current_user_id,
    )
    await session.execute(stmt)
    await session.commit()
    return True
