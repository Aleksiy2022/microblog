from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Image


async def create_media(
    session: AsyncSession,
    image_src: str,
) -> int:
    new_image = Image(src=image_src)
    session.add(new_image)
    await session.commit()
    await session.refresh(new_image)
    return new_image.id


async def update_data_medias(
    session: AsyncSession, tweet_id: int, tweet_media_ids: list[int]
) -> None:
    await session.execute(
        update(Image),
        [{"id": id, "tweet_id": tweet_id} for id in tweet_media_ids],
    )
    await session.commit()
