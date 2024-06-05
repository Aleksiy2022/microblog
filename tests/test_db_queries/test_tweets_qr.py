import pytest
from fastapi import HTTPException
from sqlalchemy import select

from api.core import test_db_helper
from api.db import Tweet, tweets_qr


@pytest.mark.asyncio(scope="session")
async def test_get_all_tweets():
    session = test_db_helper.get_scoped_session()
    result = await tweets_qr.get_all_tweets(
        session=session,
    )
    await session.close()
    assert type(result) is list
    assert len(result) == 7


@pytest.mark.asyncio(scope="session")
async def test_create_tweet():
    session = test_db_helper.get_scoped_session()
    result = await tweets_qr.create_tweet(
        session=session,
        tweet_content="Some text",
        current_user_id=2,
    )
    await session.close()

    stmt = select(Tweet).where(Tweet.id == result, Tweet.user_id == 2)
    test_tweet = await session.scalar(stmt)
    await session.close()

    assert result == 9
    assert test_tweet.content == "Some text"


@pytest.mark.parametrize(
    "tweet_id, user_id, exp_result",
    [
        (9, 2, True),
        (20, 2, False),
    ]
)
@pytest.mark.asyncio(scope="session")
async def test_delete_tweet(tweet_id, user_id, exp_result):
    session = test_db_helper.get_scoped_session()
    result = await tweets_qr.delete_tweet(
        session=session, tweet_id=tweet_id, current_user_id=user_id
    )
    await session.close()
    assert result == exp_result
