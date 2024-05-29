import pytest
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from twitter_api.core import test_db_helper
from twitter_api.db import TweetLike, likes_qr


@pytest.mark.asyncio(scope="session")
async def test_create_tweet_like():
    session = test_db_helper.get_scoped_session()
    stmt = select(TweetLike)
    tweet_likes = await session.scalars(stmt)
    before_tweet_likes = len(list(tweet_likes))
    result = await likes_qr.create_tweet_like(
        session=session, tweet_id=4, current_user_id=5
    )
    await session.close()

    tweet_likes = await session.scalars(stmt)
    after_tweet_likes = len(list(tweet_likes))
    await session.close()

    assert result is True
    assert before_tweet_likes == after_tweet_likes - 1


@pytest.mark.asyncio(scope="session")
async def test_create_tweet_like_errors():
    session = test_db_helper.get_scoped_session()
    with pytest.raises(HTTPException) as excinfo:
        await likes_qr.create_tweet_like(
            session=session, tweet_id=4, current_user_id=5
        )
    await session.close()

    with pytest.raises(HTTPException) as another_excinfo:
        await likes_qr.create_tweet_like(
            session=session, tweet_id=100, current_user_id=5
        )

    assert "You have already liked this tweet." in str(excinfo.value)
    assert "Tweet with id: 100 does not exist." in str(another_excinfo.value)


@pytest.mark.asyncio(scope="session")
async def test_delete_tweet_like():
    session: AsyncSession = test_db_helper.get_scoped_session()
    stmt = select(TweetLike)
    tweet_likes = await session.scalars(stmt)
    before_tweet_likes = len(list(tweet_likes))
    result = await likes_qr.delete_tweet_like(
        session=session, tweet_id=4, current_user_id=5
    )
    await session.close()

    tweet_likes = await session.scalars(stmt)
    after_tweet_likes = len(list(tweet_likes))
    await session.close()

    assert result is True
    assert before_tweet_likes == after_tweet_likes + 1


@pytest.mark.asyncio(scope="session")
async def test_delete_tweet_like_errors():
    session: AsyncSession = test_db_helper.get_scoped_session()
    with pytest.raises(HTTPException) as excinfo:
        await likes_qr.delete_tweet_like(
            session=session, tweet_id=100, current_user_id=5
        )
    await session.close()
    assert "Tweet_like does not exist." in str(excinfo.value)
