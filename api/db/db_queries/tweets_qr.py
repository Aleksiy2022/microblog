from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models import Image, Tweet


async def get_tweet(
    session: AsyncSession,
    tweet_id: int,
) -> Tweet | None:
    """
    Retrieve a tweet by its ID.

    Parameters
    ----------
    session : AsyncSession
        The asynchronous session for database operations.
    tweet_id : int
        The ID of the tweet to retrieve.

    Returns
    -------
    Tweet
        The tweet object if found, otherwise None.
    """
    tweet_stmt = select(Tweet).where(Tweet.id == tweet_id)
    return await session.scalar(tweet_stmt)


async def get_all_tweets(session: AsyncSession) -> list[Tweet]:
    """
    Retrieve all tweets from the database.

    This function retrieves all tweets from the database in descending order
    of their creation date. It also loads related entities, such as the author,
    likes, and attachments with optimized loading strategies.

    Parameters
    ----------
    session : AsyncSession
        The asynchronous session for database operations.

    Returns
    -------
    list of Tweet
        A list of Tweet objects representing the retrieved tweets.
    """
    stmt = (
        select(Tweet)
        .options(
            selectinload(Tweet.author),
            selectinload(Tweet.tweet_likes),
            selectinload(Tweet.attachments).load_only(Image.src),
        )
        .order_by(Tweet.created_at.desc())
    )
    tweets = await session.scalars(stmt)
    return list(tweets)


async def create_tweet(
    session: AsyncSession,
    tweet_content: str,
    current_user_id: int,
) -> int:
    """
    Create a new tweet in the database.

    This function creates a new tweet with the specified content and associates
    it with the current user. After committing the transaction, it returns the
    ID of the newly created tweet.

    Parameters
    ----------
    session : AsyncSession
        The asynchronous session for database operations.
    tweet_content : str
        The content of the tweet.
    current_user_id : int
        The ID of the user creating the tweet.

    Returns
    -------
    int
        The ID of the newly created tweet.
    """
    tweet = Tweet(
        content=tweet_content,
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
    """
    Delete a tweet from the database.

    This function deletes a tweet with the specified ID, if it belongs to the
    current user. If the tweet does not exist or does not belong to the user,
    an HTTP 404 exception is raised.

    Parameters
    ----------
    session : AsyncSession
        The asynchronous session for database operations.
    tweet_id : int
        The ID of the tweet to be deleted.
    current_user_id : int
        The ID of the user attempting to delete the tweet.

    Returns
    -------
    bool
        True if the tweet was successfully deleted, otherwise False. If the tweet does
        not exist or does not belong to the current user, the function returns False.

    """
    stmt = select(Tweet).where(
        Tweet.id == tweet_id,
        Tweet.user_id == current_user_id,
    )
    tweet = await session.scalar(stmt)
    if not tweet:
        return False

    await session.delete(tweet)
    await session.commit()
    return True
