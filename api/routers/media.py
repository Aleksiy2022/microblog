from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import medias_qr
from ..dependencies import scoped_session_db
from .router_helpers import save_tweet_image

router = APIRouter(
    prefix="/api/medias",
    tags=["media"],
)


@router.post("/")
async def load_media(
    file: Annotated[UploadFile, File()],
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
):
    """
    Upload and save a media file.

    This endpoint allows uploading a media file. The file is saved and a record is created in the
    database. Only supported file types are allowed.

    Parameters
    ----------
    file : UploadFile
        The media file to be uploaded.

    session : AsyncSession
        The database session used for creating the media record.

    Returns
    -------
    dict
        A dictionary containing the result status and the ID of the created media record.

    Raises
    ------
    HTTPException
        If the file type is not supported, a 415 Unsupported Media Type status will be returned.
    """
    image_src: str = await save_tweet_image(file)  # type: ignore

    if not image_src:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="File type not supported",
        )

    media = await medias_qr.create_media(
        session,
        image_src=image_src,
    )

    return {
        "result": True,
        "media_id": media.id,
    }
