import os

import aiofiles  # type: ignore
from fastapi import UploadFile
from fastapi.exceptions import RequestValidationError

from ..core import settings


async def save_tweet_image(image: UploadFile) -> str:
    file_name: str | None = image.filename
    if file_name is None:
        raise RequestValidationError(errors=[], body="No file name")
    file_path = os.path.join(settings.dir_uploaded_images, file_name)
    async with aiofiles.open(file_path, "wb") as f:
        content = await image.read()
        await f.write(content)
    return os.path.join("tweets_images", file_name)
