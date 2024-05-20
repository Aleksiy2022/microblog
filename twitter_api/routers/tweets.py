from typing import Annotated

from fastapi import APIRouter, Body, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import likes_qr, medias_qr, schemas, tweets_qr
from ..dependencies import get_current_user_by_api_key, scoped_session_db

router = APIRouter(
    prefix="/api/tweets",
    tags=["tweets"],
)


@router.api_route(
    "/{id}/likes",
    methods=["POST", "DELETE"],
)
async def tweet_likes(
    id: int,
    request: Request,
    current_user: Annotated[
        schemas.UserOut, Depends(get_current_user_by_api_key)
    ],
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
):
    if request.method == "POST":
        if await likes_qr.create_tweet_like(
            session,
            tweet_id=id,
            current_user_id=current_user.id,
        ):
            return {
                "result": True,
            }
    elif request.method == "DELETE":
        if await likes_qr.delete_tweet_like(
            session,
            tweet_id=id,
            current_user_id=current_user.id,
        ):
            return {
                "result": True,
            }


@router.get(
    "/",
    response_model=schemas.TweetsResponse,
)
async def get_tweets(
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
):
    tweets = await tweets_qr.get_all_tweets(session)
    tweets_response = [
        {
            "id": tweet.id,
            "content": tweet.content,
            "attachments": [att.src for att in tweet.attachments],
            "author": tweet.author,
            "likes": tweet.tweet_likes,
        }
        for tweet in tweets
    ]
    return {
        "result": True,
        "tweets": tweets_response,
    }


@router.post("/")
async def create_tweet(
    tweet_data: Annotated[str, Body()],
    tweet_media_ids: Annotated[list[int] | None, Body()],
    current_user: Annotated[
        schemas.UserOut, Depends(get_current_user_by_api_key)
    ],
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
):
    tweet_id = await tweets_qr.create_tweet(
        session,
        content=tweet_data,
        current_user_id=current_user.id,
    )
    if tweet_media_ids:
        await medias_qr.update_data_medias(
            session,
            tweet_id=tweet_id,
            tweet_media_ids=tweet_media_ids,
        )
    return {
        "result": True,
        "tweet_id": tweet_id,
    }


@router.delete("/{id}")
async def delete_tweet(
    id: int,
    current_user: Annotated[
        schemas.UserOut, Depends(get_current_user_by_api_key)
    ],
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
):
    if await tweets_qr.delete_tweet(
        session,
        tweet_id=id,
        current_user_id=current_user.id,
    ):
        return {
            "result": True,
        }
