from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Image


async def create_media(
    session: AsyncSession,
    image_src: str,
) -> Image:
    """
    Create a new media entry in the database.

    This function creates a new media object with the given image source URL,
    stores it in the database, and returns the created media object.

    Parameters
    ----------
    session : AsyncSession
        The asynchronous session for database operations.
    image_src : str
        The URL or path to the image source that will be stored in the database.

    Returns
    -------
    Image
        The newly created media object.
    """
    new_image = Image(src=image_src)
    session.add(new_image)
    await session.commit()
    await session.refresh(new_image)
    return new_image


async def update_data_medias(
    session: AsyncSession,
    tweet_id: int,
    tweet_media_ids: list[int],
) -> None:
    """
    Update media entries with a tweet ID in the database.

    This function updates multiple media objects with the given tweet ID,
    associating each media object with the tweet.

    Parameters
    ----------
    session : AsyncSession
        The asynchronous session for database operations.
    tweet_id : int
        The ID of the tweet to associate with the media entries.
    tweet_media_ids : list of int
        A list of media IDs that need to be updated with the tweet ID.
    """
    await session.execute(
        update(Image),
        [{"id": id, "tweet_id": tweet_id} for id in tweet_media_ids],
    )
    await session.commit()
