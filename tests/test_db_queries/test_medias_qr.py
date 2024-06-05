import pytest
from sqlalchemy import select

from api.core import test_db_helper
from api.db import Image, medias_qr


@pytest.mark.asyncio(scope="session")
async def test_create_media():
    session = test_db_helper.get_scoped_session()
    test_file_name = "test_images/image.jpg"
    image = await medias_qr.create_media(session=session, image_src=test_file_name)
    await session.commit()
    await session.close()
    assert image.id == 2


@pytest.mark.asyncio(scope="session")
async def test_update_data_medias():
    test_tweet_id = 2
    session = test_db_helper.get_scoped_session()
    await medias_qr.update_data_medias(session=session, tweet_id=test_tweet_id, tweet_media_ids=[2])
    await session.close()

    stmt = select(Image).where(
        Image.id == 2,
        Image.src == "test_images/image.jpg",
    )
    image = await session.scalar(stmt)
    await session.close()
    assert image.tweet_id == test_tweet_id
