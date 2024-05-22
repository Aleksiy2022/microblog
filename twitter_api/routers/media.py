from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import medias_qr
from ..dependencies import scoped_session_db
from .utils import save_tweet_image

router = APIRouter(
    prefix="/api/medias",
    tags=["media"],
)


@router.post("/")
async def load_media(
    file: Annotated[UploadFile, File()],
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
):
    try:
        image_src = await save_tweet_image(file)
        media_id = await medias_qr.create_media(
            session,
            image_src=image_src,
        )

        return {
            "result": True,
            "media_id": media_id,
        }
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to load image")
