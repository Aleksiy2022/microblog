from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Tweet, TweetLike


async def create_tweet_like(
    session: AsyncSession,
    tweet_id: int,
    current_user_id: int,
) -> bool:
    stmt = select(Tweet).where(Tweet.id == tweet_id)
    tweet = await session.scalar(stmt)
    if tweet:
        stmt = select(TweetLike).where(
                TweetLike.tweet_id == tweet_id,
                TweetLike.user_id == current_user_id,
            )
        tweet_like = await session.scalar(stmt)
        if not tweet_like:
            new_tweet_like = TweetLike(
                tweet_id=tweet_id,
                user_id=current_user_id,
            )
            session.add(new_tweet_like)
            await session.commit()
            return True
        else:
            raise HTTPException(
                status_code=409, detail="You have already liked this tweet."
            )
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Tweet with id: {tweet_id} does not exist.",
        )


async def delete_tweet_like(
    session: AsyncSession, tweet_id: int, current_user_id: int
) -> bool:
    stmt = select(TweetLike).where(
        TweetLike.tweet_id == tweet_id, TweetLike.user_id == current_user_id
    )
    tweet_like = await session.scalar(stmt)
    if tweet_like:
        await session.delete(tweet_like)
        await session.commit()
        return True
    else:
        raise HTTPException(
            status_code=404, detail="Tweet_like does not exist."
        )
