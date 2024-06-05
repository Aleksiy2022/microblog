import pytest
from fastapi import HTTPException


@pytest.mark.parametrize(
    "tweet_id, expected_status, exp_response_json",
    [
        (
            1,
            200,
            {
                "result": True,
            },
        ),  # create new tweet_like with correct data
        (
            -1,
            422,
            {
                "result": False,
                "error_type": "greater_than_equal",
                "error_message": "Input should be greater than or equal to 1",
            },
        ),  # test id validation ge
        (
            1, 404,
            {
                "result": False,
                "error_type": "HTTPException",
                "error_message": "Tweet with id: 1 does not exist or you have already liked this tweet."
            },
        ),  # test raise exception
        (
            20, 404,
            {
                "result": False,
                "error_type": "HTTPException",
                "error_message": "Tweet with id: 20 does not exist or you have already liked this tweet."
            },  # try to like non-existing tweet
        ),
    ],
)
@pytest.mark.asyncio(scope="session")
async def test_create_tweet_likes(
    async_client, tweet_id, expected_status, exp_response_json
):
    headers = {"Api-Key": "test"}
    response = await async_client.post(
        f"http://127.0.0.1:8000/api/tweets/{tweet_id}/likes",
        headers=headers,
    )
    assert response.status_code == expected_status
    assert response.json() == exp_response_json


@pytest.mark.parametrize(
    "tweet_id, expected_status, exp_response_json",
    [
        (
            1,
            200,
            {
                "result": True,
            },
        ),  # test existing tweet id
        (
            -1,
            422,
            {
                "result": False,
                "error_type": "greater_than_equal",
                "error_message": "Input should be greater than or equal to 1",
            },
        ),  # test id validation ge
(
            20, 404,
            {
                "result": False,
                "error_type": "HTTPException",
                "error_message": "A tweet like with id: 20 does not exist."
            },
        )  # test raise exception
    ],
)
@pytest.mark.asyncio(scope="session")
async def test_delete_tweet_likes(
    async_client, tweet_id, expected_status, exp_response_json
):
    headers = {"Api-Key": "test"}
    response = await async_client.delete(
        f"http://127.0.0.1:8000/api/tweets/{tweet_id}/likes",
        headers=headers,
    )
    assert response.status_code == expected_status
    assert response.json() == exp_response_json


@pytest.mark.asyncio(scope="session")
async def test_get_tweets(async_client):
    headers = {"Api-Key": "test"}
    response = await async_client.get(
        "http://127.0.0.1:8000/api/tweets/",
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json().get("result") is True
    assert len(response.json().get("tweets")) == 6
    for tweet in response.json().get("tweets"):
        assert ("id", "content", "attachments", "author", "likes") == tuple(
            tweet.keys()
        )


@pytest.mark.parametrize(
    "tweet_data, tweet_media_ids, expected_status, exp_response_json",
    [
        (
            "Test tweet",
            [],
            200,
            {
                "result": True,
                "tweet_id": 7,
            },
        ),  # Test without images
        (
            "This is another test tweet",
            [1, 2],
            200,
            {
                "result": True,
                "tweet_id": 8,
            },
        ),  # Test with images
        (
            "A" * 501,
            [3],
            422,
            {
                "result": False,
                "error_type": "string_too_long",
                "error_message": "String should have at most 500 characters",
            },
        ),  # Test for max_length constraint
    ],
)
@pytest.mark.asyncio(scope="session")
async def test_create_tweet(
    async_client,
    tweet_data,
    tweet_media_ids,
    expected_status,
    exp_response_json,
):
    headers = {"Api-Key": "test"}
    response = await async_client.post(
        "http://127.0.0.1:8000/api/tweets/",
        headers=headers,
        json={
            "tweet_data": tweet_data,
            "tweet_media_ids": tweet_media_ids,
        },
    )
    assert response.status_code == expected_status
    assert response.json() == exp_response_json


@pytest.mark.parametrize(
    "tweet_id, expected_status, exp_response_json",
    [
        (
            -1,
            422,
            {
                "result": False,
                "error_type": "greater_than_equal",
                "error_message": "Input should be greater than or equal to 1",
            },
        ),  # test with tweet_id less than 1
        (
            1,
            200,
            {
                "result": True,
            },
        ),  # test with correct data
        (
            2,
            404,
            {
                "result": False,
                "error_type": "HTTPException",
                "error_message": "Tweet doesn't exist "
                "or doesn't belong to you",
            },
        ),  # test deleting a tweet that does not belong to the current user
        (
            10,
            404,
            {
                "result": False,
                "error_type": "HTTPException",
                "error_message": "Tweet doesn't exist "
                "or doesn't belong to you",
            },
        ),  # test with not existing tweet_id
    ],
)
@pytest.mark.asyncio(scope="session")
async def test_delete_tweet(
    async_client, tweet_id, expected_status, exp_response_json
):
    headers = {"Api-Key": "test"}
    response = await async_client.delete(
        f"http://127.0.0.1:8000/api/tweets/{tweet_id}", headers=headers
    )
    assert response.status_code == expected_status
    assert response.json() == exp_response_json
