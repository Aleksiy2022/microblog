import pytest


@pytest.mark.parametrize(
    "api_key, exr_status_code, exp_response_json",
    [
        (
            "test", 200,
            {
                "result": True,
                "user": {
                    "id": 1,
                    "name": "Aleksiy",
                    "followers": [],
                    "following": []
                }
            }
         ),  # test with correct data
        (
            "some_wrong_api_key", 404,
            {
                "result": False,
                "error_type": "HTTPException",
                "error_message": "User with api_key: some_wrong_api_key not found"
            }
        ),  # test with incorrect api_key
        (
            "some_very_very_long_wrong_api_key", 422,
            {
                "result": False,
                "error_type": "string_too_long",
                "error_message": "String should have at most 30 characters"
            }
        ),  # test with an api_key exceeding the allowed number of characters
    ]
)
@pytest.mark.asyncio(scope="session")
async def test_current_user_profile(async_client, api_key, exr_status_code, exp_response_json):
    headers = {"Api-Key": api_key}
    response = await async_client.get(
        f"http://127.0.0.1:8000/api/users/me",
        headers=headers,
    )
    assert response.json() == exp_response_json
    assert response.status_code == exr_status_code


@pytest.mark.parametrize(
    "user_id, exr_status_code, exp_response_json",
    [
        (
            -1, 422,
            {
                "result": False,
                "error_type": "greater_than_equal",
                "error_message": "Input should be greater than or equal to 1",
            },
        ),  # test with user_id less than 1
        (
            2, 200,
            {
                "result": True,
            },
        ),  # test with correct data
        (
            2, 409,
            {
                "result": False,
                "error_type": "HTTPException",
                "error_message": "You have already subscribed to this user with id: 2",
            },
        ),  # try to subscribe to the user again
        (
            100, 404,
            {
                "result": False,
                "error_type": "HTTPException",
                "error_message": "User with id: 100 not found",
            },
        )
    ]
)
@pytest.mark.asyncio(scope="session")
async def test_create_user_following_node(async_client, user_id, exr_status_code, exp_response_json):
    headers = {"Api-Key": "test"}
    response = await async_client.post(
        f"http://127.0.0.1:8000/api/users/{user_id}/follow",
        headers=headers,
    )
    assert response.json() == exp_response_json
    assert response.status_code == exr_status_code


@pytest.mark.parametrize(
    "user_id, exr_status_code, exp_response_json",
    [
        (
            -1, 422,
            {
                "result": False,
                "error_type": "greater_than_equal",
                "error_message": "Input should be greater than or equal to 1",
            },
        ),  # test with user_id less than 1
        (
            2, 200,
            {
                "result": True,
            }
        ),  # test with correct data
        (
            2, 404,
            {
                "result": False,
                "error_type": "HTTPException",
                "error_message": "You are not subscribed to a user with id 2",
            }
        ),  # try to sign from the user again
    ]
)
@pytest.mark.asyncio(scope="session")
async def test_delete_user_following_node(async_client, user_id, exr_status_code, exp_response_json):
    headers = {"Api-Key": "test"}
    response = await async_client.delete(
        f"http://127.0.0.1:8000/api/users/{user_id}/follow",
        headers=headers,
    )
    assert response.json() == exp_response_json
    assert response.status_code == exr_status_code


@pytest.mark.parametrize(
    "user_id, exr_status_code, exp_response_json",
    [
        (
            -1, 422,
            {
                "result": False,
                "error_type": "greater_than_equal",
                "error_message": "Input should be greater than or equal to 1",
            },
        ),  # test with user_id less than 1
        (
            1, 200,
            {
                "result": True,
                "user": {
                    "id": 1,
                    "name": "Aleksiy",
                    "followers": [],
                    "following": []
                }
            }
        ),  # test with correct data
        (
            10, 404,
            {
                "result": False,
                "error_type": "HTTPException",
                "error_message": "User with id: 10 not found",
            },
        ),  # test with not existing user_id
    ]
)
@pytest.mark.asyncio(scope="session")
async def test_user_profile(async_client, user_id, exr_status_code, exp_response_json):
    response = await async_client.get(
        f"http://127.0.0.1:8000/api/users/{user_id}",
    )
    assert response.json() == exp_response_json
    assert response.status_code == exr_status_code
