from fastapi import APIRouter

router = APIRouter(
    prefix="/api/tweets",
    tags=["tweets"],
)


@router.post("/")
async def create_tweet():
    return {}
