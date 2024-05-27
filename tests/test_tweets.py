import pytest


@pytest.mark.parametrize(
    "tweet_data, tweet_media_ids, expected_status",
    [
        ("Test tweet", [], 200),
        ("This is another test tweet", [1, 2], 200),
        ("A" * 501, [3], 422),  # Test for max_length constraint
    ]
)
@pytest.mark.asyncio(scope="session")
async def test_create_tweet(async_client, tweet_data, tweet_media_ids, expected_status):
    headers = {"Api-Key": "test"}
    response = await async_client.post(
        "http://127.0.0.1:8000/api/tweets/",
        headers=headers,
        json={
            "tweet_data": tweet_data,
            "tweet_media_ids": tweet_media_ids
        }
    )
    assert response.status_code == expected_status
