from fastapi import APIRouter

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)


@router.get("/me")
async def get_tweets():
    return {
        "result": "true",
        "user": {
            "id": 1,
            "name": "Ivan",
            "followers": [{"id": 2, "name": "Oleg"}],
            "following": [{"id": 3, "name": "Kirill"}],
        },
    }
