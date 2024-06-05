from typing import Annotated, AsyncGenerator

from fastapi import Depends, Header
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .core import db_helper
from .db import User, users_qr


async def scoped_session_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide a scoped database session for FastAPI endpoints.

    This dependency creates a new session for each request and ensures it is closed after use.

    Yields
    ------
    AsyncSession
        An asynchronous session object for database operations.
    """
    session = db_helper.get_scoped_session()
    try:
        yield session
    finally:
        await session.close()


async def get_current_user_by_api_key(
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
    api_key: Annotated[str, Header(max_length=30)],
) -> User:
    """
    Get the current user based on the provided API key.

    This dependency retrieves a user from the database using an API key from the request's header.
    If the user is not found, an HTTP 404 error is raised.

    Parameters
    ----------
    session : AsyncSession
        The scoped asynchronous session for database operations, provided by `scoped_session_db`.
    api_key : str
        The API key provided in the request header (max length 30).

    Returns
    -------
    User
        The user object corresponding to the provided API key.

    Raises
    ------
    HTTPException
        If no user is found with the provided API key
    """
    user = await users_qr.get_current_user(session, api_key=api_key)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with api_key: {api_key} not found",
        )
    return user
