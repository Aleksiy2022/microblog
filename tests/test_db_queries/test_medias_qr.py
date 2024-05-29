import pytest
from sqlalchemy import select

from twitter_api.core import test_db_helper
from twitter_api.db import Image, medias_qr


@pytest.mark.asyncio(scope="session")
async def test_create_media():
    session = test_db_helper.get_scoped_session()
    test_file_name = (
        "tweets_images_for_tests/1651174528_1-sportishka-"
        "com-p-mashina-porshe-mashini-krasivo-foto-1.jpg"
    )
    result = await medias_qr.create_media(
        session=session, image_src=test_file_name
    )
    await session.commit()
    await session.close()
    assert result == 1


@pytest.mark.asyncio(scope="session")
async def test_update_data_medias():
    test_tweet_id = 1
    session = test_db_helper.get_scoped_session()
    await medias_qr.update_data_medias(
        session=session, tweet_id=test_tweet_id, tweet_media_ids=[1]
    )
    await session.close()

    stmt = select(Image).where(
        Image.id == 1,
        Image.src == "tweets_images_for_tests/1651174528_1-sportishka"
        "-com-p-mashina-porshe-mashini-krasivo-foto-1.jpg",
    )
    image = await session.scalar(stmt)
    await session.close()
    assert image.tweet_id == test_tweet_id
