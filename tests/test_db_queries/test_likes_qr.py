import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.core import test_db_helper
from api.db import TweetLike, likes_qr


@pytest.mark.parametrize(
    "action, tweet_id, user_id, likes_before, likes_after, exp_result",
    [
        ("create", 4, 5, 1, 2, True),  # try to like with correct data
        ("create", 4, 5, 2, 2, False),  # try to like the same tweet
        ("create", 10, 5, 2, 2, False),  # try to like a non-existent tweet
        ("delete", 4, 5, 2, 1, True),  # try to delete like with correct data
        ("delete", 4, 5, 1, 1, False),  # try to delete like the same tweet
        ("delete", 10, 5, 1, 1, False),  # try to delete a like from a non-existent tweet
    ]
)
@pytest.mark.asyncio(scope="session")
async def test_create_tweet_like(action, tweet_id, user_id, likes_before, likes_after, exp_result):
    session = test_db_helper.get_scoped_session()
    stmt = select(TweetLike)
    tweet_likes = await session.scalars(stmt)
    before_tweet_likes = len(list(tweet_likes))

    if action == "create":
        result = await likes_qr.create_tweet_like(
            session=session, tweet_id=tweet_id, current_user_id=user_id
        )
    else:
        result = await likes_qr.delete_tweet_like(
            session=session, tweet_id=tweet_id, current_user_id=user_id
        )

    await session.close()

    tweet_likes = await session.scalars(stmt)
    after_tweet_likes = len(list(tweet_likes))
    await session.close()

    assert result == exp_result
    assert before_tweet_likes == likes_before
    assert after_tweet_likes == likes_after
