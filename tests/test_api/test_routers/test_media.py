import io
import os

import aiofiles
import pytest

path = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.parametrize(
    "image_path, image_name, exp_response",
    [
        (
            os.path.join(
                path, "test_images", "light_image.jpg"
            ),
            "light_image.jpg",
            {
                'result': True,
                'media_id': 1
            }
        ),  # test with correct data
        (
            os.path.join(
                path, "test_images", "heavy_image.png"
            ),
            "heavy_image.jpg",
            {
                "result": False,
                'error_type': 'error max size',
                'error_message': 'File too large. Maximum allowed size is 1MB',
            }  # test with an image exceeding 1 mb
        ),
        (
            os.path.join(
                path, "test_images", "not_image.txt"
            ),
            "not_image.txt",
            {
                'result': False,
                'error_type': 'HTTPException',
                'error_message': 'File type not supported'
            }  # test with a file that is not an image
        ),
    ]
)
@pytest.mark.asyncio(scope="session")
async def test_load_media(async_client, image_path, image_name, exp_response):
    async with aiofiles.open(image_path, "rb") as image_file:
        image_data = await image_file.read()
        image_io = io.BytesIO(image_data)

    response = await async_client.post(
        "http://127.0.0.1:8000/api/medias/",
        files={"file": (image_name, image_io)}
    )
    assert response.json() == exp_response


