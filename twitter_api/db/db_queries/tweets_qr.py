from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Tweet, Image
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from .users_qr import get_current_user_id


async def get_tweets_user_followings(session: AsyncSession, api_key) -> list[Tweet]:
    # stmt = (
    #     select(Tweet).
    #     join(Follower, Tweet.user_id == Follower.user_id).
    #     join(User, User.id == Follower.follower).
    #     options(
    #         selectinload(Tweet.author),
    #         selectinload(Tweet.tweet_likes),
    #         selectinload(Tweet.attachments).load_only(Image.src),
    #     ).
    #     where(User.api_key == api_key)
    # )
    stmt = (
        select(Tweet).
        options(
            selectinload(Tweet.author),
            selectinload(Tweet.tweet_likes),
            selectinload(Tweet.attachments).load_only(Image.src),
        )
    )
    tweets = await session.scalars(stmt)
    return list(tweets)


async def create_tweet(
        session: AsyncSession,
        content: str = None,
        user_id: int = None,
) -> int:
    tweet = Tweet(
        content=content,
        user_id=user_id,
    )
    session.add(tweet)
    await session.commit()
    await session.refresh(tweet)
    return tweet.id


async def delete_tweet(session: AsyncSession, tweet_id: int = None, api_key: str = None) -> bool:
    user_id = await get_current_user_id(session, api_key=api_key)
    stmt = delete(Tweet).where(Tweet.id == tweet_id, Tweet.user_id == user_id)
    await session.execute(stmt)
    await session.commit()
    return True
