from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import UserOut, likes_qr, medias_qr, schemas, tweets_qr
from ..dependencies import get_current_user_by_api_key, scoped_session_db

router = APIRouter(
    prefix="/api/tweets",
    tags=["tweets"],
)


@router.post("/{id}/likes")
async def create_tweet_likes(
    id: Annotated[int, Path(ge=1)],
    current_user: Annotated[UserOut, Depends(get_current_user_by_api_key)],
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
):
    """
    Create a like for the specified tweet.

    Parameters
    ----------
    id : int
        The ID of the tweet to be liked (must be >= 1).
    current_user : UserOut
        An object representing the currently authenticated user.
    session : AsyncSession
        The database session for executing operations.

    Returns
    -------
    dict
        A JSON object with a key "result" and value True if the like was successfully created.

    Raises
    ------
    HTTPException
        If the tweet does not exist or the user has already liked the tweet.
        Status code: 404, detail: "Tweet with id: {id} does not exist or you have already
        liked this tweet."
    """
    result = await likes_qr.create_tweet_like(
        session,
        tweet_id=id,
        current_user_id=current_user.id,
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tweet with id: {id} does not exist or you have already liked this tweet.",
        )
    return {"result": True}


@router.delete("/{id}/likes")
async def delete_tweet_like(
    id: Annotated[int, Path(ge=1)],
    current_user: Annotated[UserOut, Depends(get_current_user_by_api_key)],
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
):
    """
    Delete a like for the specified tweet.

    Parameters
    ----------
    id : int
        The ID of the tweet for which the like should be deleted (must be >= 1).
    current_user : UserOut
        Object representing the currently authenticated user.
    session : AsyncSession
        Database session for performing operations.

    Returns
    -------
    dict
        JSON object with a key "result" and value True if the like was successfully deleted.

    Raises
    ------
    HTTPException
        If the tweet does not exist:
        - Status code: 404, detail: "A tweet like with id: {id} does not exist."
    """
    result = await likes_qr.delete_tweet_like(
        session,
        tweet_id=id,
        current_user_id=current_user.id,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"A tweet like with id: {id} does not exist.",
        )
    return {"result": True}


@router.get("/", response_model=schemas.TweetsResponse)
async def get_tweets(
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
):
    """
    Retrieve a list of all tweets.

    Parameters
    ----------
    session : AsyncSession
        Database session for performing operations.

    Returns
    -------
    dict
        JSON object containing the key "result" with the value True and the key "tweets"
        with a list of all tweets.
    """
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
    tweet_data: Annotated[str, Body(max_length=500)],
    tweet_media_ids: Annotated[list[int], Body()],
    current_user: Annotated[UserOut, Depends(get_current_user_by_api_key)],
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
):
    """
    Create a new tweet.

    Parameters
    ----------
    tweet_data : str
        The content of the tweet, up to 500 characters.
    tweet_media_ids : list of int
        A list of media IDs to be associated with the tweet.
    current_user : UserOut
        The currently authenticated user creating the tweet.
    session : AsyncSession
        Database session for performing operations.

    Returns
    -------
    dict
        JSON object containing the key "result" with the value True and the key "tweet_id"
        with the ID of the created tweet.

    Raises
    ------
    HTTPException
        If there is an SQLAlchemy error during tweet creation or media update.
    """
    try:
        tweet_id = await tweets_qr.create_tweet(
            session,
            tweet_content=tweet_data,
            current_user_id=current_user.id,
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Failed to create tweet",
        )

    if tweet_media_ids:
        try:
            await medias_qr.update_data_medias(
                session,
                tweet_id=tweet_id,
                tweet_media_ids=tweet_media_ids,
            )
        except SQLAlchemyError:
            raise HTTPException(
                status_code=500,
                detail="Failed to update tweet media",
            )

    return {
        "result": True,
        "tweet_id": tweet_id,
    }


@router.delete("/{id}")
async def delete_tweet(
    id: Annotated[int, Path(ge=1)],
    current_user: Annotated[UserOut, Depends(get_current_user_by_api_key)],
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
):
    """
    Delete a tweet by its ID.

    This endpoint deletes a tweet specified by its ID if it belongs to the
    current authenticated user. The operation will fail if the tweet does not
    exist or if the tweet does not belong to the current user.

    Parameters
    ----------
    id : int
        The ID of the tweet to be deleted. Must be greater than or equal to 1.
    current_user : UserOut
        The currently authenticated user attempting to delete the tweet.
    session : AsyncSession
        The asynchronous session for database operations.

    Returns
    -------
    dict
        A JSON object containing a single key "result" with the value True
        if the tweet was successfully deleted.

    Raises
    ------
    HTTPException
        If the tweet does not exist or does not belong to the user, an HTTP
        exception with status code 404 and a corresponding error message is raised.
    """
    result = await tweets_qr.delete_tweet(
        session,
        tweet_id=id,
        current_user_id=current_user.id,
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tweet doesn't exist or doesn't belong to you",
        )
    return {"result": True}
