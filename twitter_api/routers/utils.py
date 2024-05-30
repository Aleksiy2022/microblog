import os

import aiofiles  # type: ignore
from fastapi import HTTPException, UploadFile

from ..core import settings


async def save_tweet_image(image: UploadFile) -> str:
    image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff")
    file_name: str | None = image.filename

    if file_name:
        if file_name.endswith(image_extensions):
            file_path = os.path.join(settings.dir_uploaded_images, file_name)

            async with aiofiles.open(file_path, "wb") as f:
                content = await image.read()
                await f.write(content)

            return os.path.join("tweets_images", file_name)
        else:
            raise HTTPException(
                status_code=415, detail="File type not supported"
            )
    else:
        raise HTTPException(status_code=415, detail="File type not supported")
