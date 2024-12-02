import os

import aiofiles  # type: ignore
from fastapi import UploadFile

from api import settings


async def save_tweet_image(image: UploadFile) -> str | bool:
    """
    Save the uploaded image file to the server.

    This function saves an uploaded image file to a specified directory on the server,
    validating that the file has a supported extension. If the file is saved successfully,
    it returns the relative path to the saved file. If the file type is unsupported,
    it returns False.

    Parameters
    ----------
    image : UploadFile
        The uploaded image file to be saved.

    Returns
    -------
    str | bool
        The relative path to the saved file if successful, otherwise False.
    """
    image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff")
    file_name: str | None = image.filename

    if not file_name or not file_name.lower().endswith(image_extensions):
        return False

    file_path = os.path.join(settings.dir_uploaded_images, file_name)

    async with aiofiles.open(file_path, "wb") as image_file:
        file_content = await image.read()
        await image_file.write(file_content)

    return os.path.join("tweets_images", file_name)
