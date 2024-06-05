import pytest

from api.core import test_db_helper
from api.db import User, users_qr


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
    "id, user_data",
    [
        (
            1,
            {
                "name": "Aleksiy",
                "api_key": "test",
            },
        ),
        (10, None),
    ],
)
@pytest.mark.asyncio(scope="session")
async def test_get_full_user_info_user_by_id(id, user_data):
    session = test_db_helper.get_scoped_session()
    result = await users_qr.get_user_by_id(session, id)
    await session.close()
    if user_data is None:
        assert result is None
    else:
        assert isinstance(result, User)
        assert user_data.get("name") == result.name
        assert user_data.get("api_key") == result.api_key


@pytest.mark.parametrize(
    "follower_id, user_id, exp_result",
    [
        (1, 2, True),  # try to create a new user following record
        (1, 2, False),  # try to create a record again with the same data
    ],
)
@pytest.mark.asyncio(scope="session")
async def test_create_user_following_node(follower_id, user_id, exp_result):
    session = test_db_helper.get_scoped_session()
    result = await users_qr.create_user_following_node(
        session=session,
        follower_id=follower_id,
        user_id=user_id,
    )
    await session.close()
    assert result == exp_result


@pytest.mark.parametrize(
    "follower_id, user_id, exp_result",
    [
        (1, 2, True),
        (1, 2, False),
    ],
)
@pytest.mark.asyncio(scope="session")
async def test_delete_user_following_node(follower_id, user_id, exp_result):
    session = test_db_helper.get_scoped_session()
    result = await users_qr.delete_user_following_node(
        session=session,
        follower_id=follower_id,
        user_id=user_id,
    )
    await session.close()
    assert result == exp_result
