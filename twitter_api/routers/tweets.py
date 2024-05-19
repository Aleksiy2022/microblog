from fastapi import APIRouter, Depends, Form, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
from ..db import tweets_qr, schemas, users_qr, medias_qr, likes_qr
from typing import Annotated
from ..dependencies import get_api_key, scoped_session_db

router = APIRouter(
    prefix="/api/tweets",
    tags=["tweets"],
)


@router.post("/{id}/likes")
async def create_tweet_like(
        id: int,
        session: AsyncSession = Depends(scoped_session_db),
        api_key: Any = Depends(get_api_key),
):
    if await likes_qr.create_tweet_like(session, tweet_id=id, api_key=api_key):
        return {
            "result": True
        }


@router.delete("/{id}/likes")
async def delete_tweet_like(
        id: int,
        session: AsyncSession = Depends(scoped_session_db),
        api_key: Any = Depends(get_api_key),
):
    if await likes_qr.delete_tweet_like(session, tweet_id=id, api_key=api_key):
        return {
            "result": True
        }


@router.delete("/{id}")
async def delete_tweet(
        id: int,
        session: AsyncSession = Depends(scoped_session_db)
):
    if await tweets_qr.delete_tweet(session, tweet_id=id):
        return {
            "result": True
        }


@router.get("/", response_model=schemas.TweetsResponse)
async def get_tweets(
        api_key: str = Depends(get_api_key),
        session: AsyncSession = Depends(scoped_session_db)
) -> Any:
    tweets = await tweets_qr.get_tweets_user_followings(session, api_key=api_key)
    tweets_response = [
        {
            "id": tweet.id,
            "content": tweet.content,
            "attachments": [att.src for att in tweet.attachments],
            "author": tweet.author,
            "likes": tweet.tweet_likes
        }
        for tweet in tweets
    ]
    return {
        "result": True,
        "tweets": tweets_response
    }


@router.post("/")
async def create_tweet(
        tweet_data: Annotated[str, Body()],
        tweet_media_ids: Annotated[list[int] | None, Body()],
        api_key: str = Depends(get_api_key),
        session: AsyncSession = Depends(scoped_session_db)
) -> Any:
    user_id = await users_qr.get_current_user_id(session, api_key=api_key)
    tweet_id = await tweets_qr.create_tweet(
        session,
        content=tweet_data,
        user_id=user_id,
    )
    if tweet_media_ids:
        await medias_qr.update_data_medias(session, tweet_id=tweet_id, tweet_media_ids=tweet_media_ids)
    return {
        "result": True,
        "tweet_id": tweet_id
    }
