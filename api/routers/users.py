from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import UserOut, schemas, users_qr
from ..dependencies import get_current_user_by_api_key, scoped_session_db

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)


@router.get("/me", response_model=schemas.UserResponse)
async def current_user_profile(
    current_user: Annotated[UserOut, Depends(get_current_user_by_api_key)],
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
):
    """
    Retrieve the current user's profile information.

    Parameters
    ----------
    current_user : UserOut
        The current authenticated user.
    session : AsyncSession
        The database session for executing operations.

    Returns
    -------
    dict
        A dictionary containing the result status and full user information.
        If the user is not found, an HTTP 404 exception is raised.
    """
    user = await users_qr.get_full_user_info_by_id(
        session,
        user_id=current_user.id,
    )
    return {
        "result": True,
        "user": user,
    }


@router.post("/{id}/follow")
async def create_user_following_node(
    id: Annotated[int, Path(ge=1)],
    current_user: Annotated[UserOut, Depends(get_current_user_by_api_key)],
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
):
    """
    Create a following relationship between the current user and the user specified by the `id`.

    Parameters
    ----------
    id : int
        Path parameter for user ID. Must be greater than or equal to 1.
    current_user : UserOut
        The current authenticated user.
    session : AsyncSession
        The database session for executing operations.

    Returns
    -------
    dict
        A JSON object containing a single key "result" with the value True
        if the user following node was successfully created.

    Raises
    ------
    HTTPException
        If the user specified by `id` is not found:
            - 404 status code with detail "User with id: <id> not found"
        If the current_user is already following the user specified by `id`:
            - 409 status code with detail "You have already subscribed to this user with id: <id>"
        If there is an internal server error while creating the user following node:
            - 500 status code with detail "Failed to create user_following_node"

    """
    user = await users_qr.get_user_by_id(
        session=session,
        user_id=id,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} not found",
        )
    user_follower_node = await users_qr.get_user_following_node(
        session=session,
        user_id=id,
        follower_id=current_user.id,
    )

    if user_follower_node:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"You have already subscribed to this user with id: {id}",
        )
    result = await users_qr.create_user_following_node(
        session,
        follower_id=current_user.id,
        user_id=id,
    )

    if not result:
        raise HTTPException(
            status_code=500,
            detail="Failed to create user_following_node",
        )
    return {"result": True}


@router.delete("/{id}/follow")
async def delete_user_following_node(
    id: Annotated[int, Path(ge=1)],
    current_user: Annotated[UserOut, Depends(get_current_user_by_api_key)],
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
):
    """
    Remove a following relationship between the current user and the user specified by the `id`.

    Parameters
    ----------
    id : int
        The ID of the user to unfollow. Must be greater than or equal to 1.
    current_user : UserOut
        The current authenticated user.
    session : AsyncSession
        The database session for executing operations.

    Returns
    -------
    dict
        A dictionary indicating the result of the operation. The 'result' key contains
        `True` if the operation was successful.

    Raises
    ------
    HTTPException
        If the user to unfollow is not found (404 status) or if there was any other error
        during the operation.
    """
    result = await users_qr.delete_user_following_node(
        session,
        follower_id=current_user.id,
        user_id=id,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"You are not subscribed to a user with id {id}",
        )
    return {"result": True}


@router.get("/{id}", response_model=schemas.UserResponse)
async def user_profile(
    id: Annotated[int, Path(ge=1)],
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
):
    """
    Retrieve the profile information of a user by their ID.

    Parameters
    ----------
    id : int
        Path parameter for user ID. Must be greater than or equal to 1.
    session : AsyncSession
        The database session for executing operations.

    Returns
    -------
    dict
        A dictionary containing the result of the operation:
        - 'result': Boolean indicating if the operation was successful.
        - 'user': The user profile information.

    Raises
    ------
    HTTPException
        If the user is not found (404 status).
    """
    user = await users_qr.get_full_user_info_by_id(session, user_id=id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} not found",
        )
    return {
        "result": True,
        "user": user,
    }
