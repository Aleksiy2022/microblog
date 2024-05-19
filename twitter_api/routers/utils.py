from fastapi import UploadFile
from ..core import settings
import aiofiles
import os


async def save_tweet_image(image: UploadFile) -> str:
    file_name = image.filename
    file_path = os.path.join(settings.dir_uploaded_images, file_name)
    async with aiofiles.open(file_path, "wb") as f:
        content = await image.read()
        await f.write(content)
    return os.path.join("tweets_images", file_name)
