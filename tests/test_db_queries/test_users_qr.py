import pytest
from fastapi import HTTPException

from twitter_api.core import test_db_helper
from twitter_api.db import users_qr


@pytest.mark.parametrize(
    "api_key, exp_result",
    [
        ("test", 1),
        ("some_wrong_key", None),
    ],
)
@pytest.mark.asyncio(scope="session")
async def test_get_current_user(api_key, exp_result):
    session = test_db_helper.get_scoped_session()
    user = await users_qr.get_current_user(session, api_key)
    await session.close()
    if exp_result is None:
        assert user is None
    else:
        assert user.id == 1


@pytest.mark.parametrize(
    "id, user_obj_data",
    [
        (
            1,
            (
                "name",
                "id",
                "api_key",
                "tweets",
                "followers",
                "following",
                "tweet_likes",
            ),
        ),
        (10, None),
    ],
)
@pytest.mark.asyncio(scope="session")
async def test_get_user_by_id(id, user_obj_data):
    session = test_db_helper.get_scoped_session()
    user = await users_qr.get_user_by_id(session, id)
    await session.close()
    if user_obj_data is None:
        assert user is None
    else:
        assert all(field in user.__dict__ for field in user_obj_data)


@pytest.mark.parametrize(
    "follower_id, user_id, exp_err_msg",
    [
        (1, 2, None),
        (1, 2, "You have already subscribed to this user with id: 2"),
        (1, 10, "User with id: 10 not found"),
    ],
)
@pytest.mark.asyncio(scope="session")
async def test_create_user_following_node(follower_id, user_id, exp_err_msg):
    session = test_db_helper.get_scoped_session()
    if exp_err_msg is None:
        result = await users_qr.create_user_following_node(
            session=session,
            follower_id=follower_id,
            user_id=user_id,
        )
        assert result is True
    else:
        with pytest.raises(HTTPException) as excinfo:
            await users_qr.create_user_following_node(
                session=session,
                follower_id=follower_id,
                user_id=user_id,
            )
        assert exp_err_msg in str(excinfo.value)
    await session.close()


@pytest.mark.parametrize(
    "follower_id, user_id, exp_err_msg",
    [
        (1, 2, None),
        (1, 2, "You are not subscribed to a user with id 2"),
    ],
)
@pytest.mark.asyncio(scope="session")
async def test_delete_user_following_node(follower_id, user_id, exp_err_msg):
    session = test_db_helper.get_scoped_session()
    if exp_err_msg is None:
        result = await users_qr.delete_user_following_node(
            session=session,
            follower_id=follower_id,
            user_id=user_id,
        )
        assert result is True
    else:
        with pytest.raises(HTTPException) as excinfo:
            await users_qr.delete_user_following_node(
                session=session,
                follower_id=follower_id,
                user_id=user_id,
            )
        assert exp_err_msg in str(excinfo.value)
    await session.close()
