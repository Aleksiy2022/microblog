from inspect import isasyncgen

import pytest
from fastapi import HTTPException

from api import dependencies
from api.core import test_db_helper


@pytest.mark.asyncio(scope="session")
async def test_scoped_session_db():
    session = dependencies.scoped_session_db()
    assert isasyncgen(session) is True


@pytest.mark.parametrize(
    "api_key, exp_err_msg",
    [
        ("test", None),
        ("some_wrong_api_key", "User with api_key: some_wrong_api_key not found"),
    ],
)
@pytest.mark.asyncio(scope="session")
async def test_get_current_user_by_api_key(api_key, exp_err_msg):
    session = test_db_helper.get_scoped_session()
    if exp_err_msg:
        with pytest.raises(HTTPException) as excinfo:
            await dependencies.get_current_user_by_api_key(session=session, api_key=api_key)
            assert exp_err_msg in str(excinfo.value)
    else:
        user = await dependencies.get_current_user_by_api_key(session=session, api_key=api_key)
        assert user.id == 1
