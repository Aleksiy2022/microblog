import pytest
from fastapi import HTTPException
from sqlalchemy import select

from twitter_api.core import test_db_helper
from twitter_api.db import Tweet, tweets_qr


@pytest.mark.asyncio(scope="session")
async def test_get_all_tweets():
    session = test_db_helper.get_scoped_session()
    result = await tweets_qr.get_all_tweets(
        session=session,
    )
    await session.close()
    assert type(result) is list
    assert len(result) == 6


@pytest.mark.asyncio(scope="session")
async def test_create_tweet():
    session = test_db_helper.get_scoped_session()
    result = await tweets_qr.create_tweet(
        session=session,
        content="Some text",
        current_user_id=2,
    )
    await session.close()

    stmt = select(Tweet).where(Tweet.id == 7, Tweet.user_id == 2)
    test_tweet = await session.scalar(stmt)
    await session.close()

    assert result == 7
    assert test_tweet.content == "Some text"


@pytest.mark.asyncio(scope="session")
async def test_delete_tweet():
    session = test_db_helper.get_scoped_session()
    result = await tweets_qr.delete_tweet(
        session=session, tweet_id=7, current_user_id=2
    )
    await session.close()
    assert result is True


@pytest.mark.parametrize(
    "tweet_id, current_user_id, exp_error_msg",
    [
        (
            100,
            2,
            "Tweet doesn't exist or doesn't belong to you",
        ),  # test with not existing tweet_id
        (
            7,
            3,
            "Tweet doesn't exist or doesn't belong to you",
        ),  # try to delete a tweet that does not belong to user
    ],
)
@pytest.mark.asyncio(scope="session")
async def test_delete_tweet_error(tweet_id, current_user_id, exp_error_msg):
    session = test_db_helper.get_scoped_session()
    with pytest.raises(HTTPException) as excinfo:
        await tweets_qr.delete_tweet(
            session=session, tweet_id=tweet_id, current_user_id=current_user_id
        )
    await session.close()
    assert exp_error_msg in str(excinfo.value)
