from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import likes_qr, medias_qr, schemas, tweets_qr
from ..dependencies import get_current_user_by_api_key, scoped_session_db

router = APIRouter(
    prefix="/api/tweets",
    tags=["tweets"],
)


@router.post("/{id}/likes")
async def create_tweet_likes(
    id: Annotated[int, Path(ge=1, le=9999999)],
    current_user: Annotated[
        schemas.UserOut, Depends(get_current_user_by_api_key)
    ],
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
):
    if await likes_qr.create_tweet_like(
        session,
        tweet_id=id,
        current_user_id=current_user.id,
    ):
        return {
            "result": True
        }


@router.delete("/{id}/likes")
async def delete_tweet_like(
    id: Annotated[int, Path(ge=1, le=9999999)],
    current_user: Annotated[
        schemas.UserOut, Depends(get_current_user_by_api_key)
    ],
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
):
    if await likes_qr.delete_tweet_like(
            session,
            tweet_id=id,
            current_user_id=current_user.id,
    ):
        return {
            "result": True
        }


@router.get(
    "/",
    response_model=schemas.TweetsResponse
)
async def get_tweets(
    session: Annotated[AsyncSession, Depends(scoped_session_db)]
):
    tweets = await tweets_qr.get_all_tweets(session)
    if not tweets:
        raise HTTPException(status_code=404, detail="No tweets found")
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
    tweet_data: Annotated[str, Body(max_length=500)],
    tweet_media_ids: Annotated[list[int] | None, Body(max_length=5)],
    current_user: Annotated[
        schemas.UserOut, Depends(get_current_user_by_api_key)
    ],
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
):
    try:
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
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


@router.delete("/{id}")
async def delete_tweet(
    id: Annotated[int, Path(ge=1, le=9999999)],
    current_user: Annotated[
        schemas.UserOut, Depends(get_current_user_by_api_key)
    ],
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
):
    try:
        if await tweets_qr.delete_tweet(
            session,
            tweet_id=id,
            current_user_id=current_user.id,
        ):
            return {
                "result": True
            }
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")
