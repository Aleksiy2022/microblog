from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import TweetLike
from .tweets_qr import get_tweet


async def get_tweet_like(
    session: AsyncSession,
    tweet_id: int,
    user_id: int,
) -> TweetLike | None:
    """
    Retrieve a tweet like from the database.

    Parameters
    ----------
    session : AsyncSession
        The asynchronous session for database operations.
    tweet_id : int
        The ID of the tweet.
    user_id : int
        The ID of the user who liked the tweet.

    Returns
    -------
    TweetLike
        The TweetLike object if exists, else None.
    """
    stmt = select(TweetLike).where(
        TweetLike.tweet_id == tweet_id,
        TweetLike.user_id == user_id,
    )

    return await session.scalar(stmt)


async def create_tweet_like(
    session: AsyncSession,
    tweet_id: int,
    current_user_id: int,
) -> bool:
    """
    Create a like for a tweet if not already liked.

    Parameters
    ----------
    session : AsyncSession
        The asynchronous session for database operations.
    tweet_id : int
        The ID of the tweet to be liked.
    current_user_id : int
        The ID of the user who is liking the tweet.

    Returns
    -------
    bool
        True if the tweet like was successfully created, False otherwise.
    """
    tweet = await get_tweet(session=session, tweet_id=tweet_id)

    if not tweet:
        return False

    tweet_like = await get_tweet_like(session, tweet_id, current_user_id)

    if tweet_like:
        return False

    new_tweet_like = TweetLike(
        tweet_id=tweet_id,
        user_id=current_user_id,
    )
    session.add(new_tweet_like)
    await session.commit()
    return True


async def delete_tweet_like(
    session: AsyncSession,
    tweet_id: int,
    current_user_id: int,
) -> bool:
    """
    Delete a like for a tweet if it exists.

    Parameters
    ----------
    session : AsyncSession
        The asynchronous session for database operations.
    tweet_id : int
        The ID of the tweet whose like is to be deleted.
    current_user_id : int
        The ID of the user who is unliking the tweet.

    Returns
    -------
    bool
        True if the tweet like was successfully deleted, False otherwise.
    """
    tweet_like = await get_tweet_like(
        session=session,
        tweet_id=tweet_id,
        user_id=current_user_id,
    )

    if not tweet_like:
        return False
    await session.delete(tweet_like)
    await session.commit()
    return True
