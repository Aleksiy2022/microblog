from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from ..models import Follower, User


async def get_user_by_id(
    session: AsyncSession,
    user_id: int,
) -> User | None:
    """
    Retrieve a user by their ID from the database.

    Parameters
    ----------
    session : AsyncSession
        The database session for executing operations.
    user_id : int
        The ID of the user to be retrieved.

    Returns
    -------
    User or None
        The user object if found, otherwise None.
    """
    user_stmt = select(User).where(User.id == user_id)
    return await session.scalar(user_stmt)


async def get_current_user(
    session: AsyncSession,
    api_key: str,
) -> User | None:
    """
    Retrieve the current user based on the provided API key.

    This function attempts to fetch a user from the database associated with
    the given API key. If no user is found, it returns None.

    Parameters
    ----------
    session : AsyncSession
        The asynchronous session for database operations.
    api_key : str
        The API key used to authenticate and identify the user.

    Returns
    -------
    User | None
        The user object if a matching user is found, else None.
    """
    stmt = select(User).where(User.api_key == api_key)
    user: User | None = await session.scalar(stmt)
    return user if user else None


async def get_full_user_info_by_id(session: AsyncSession, user_id: int) -> User | None:
    """
    Retrieve a user based on the provided user ID.

    This function fetches a user from the database using their user ID. The
    resulting user includes their followers and following relationships.
    If no user is found, it returns None.

    Parameters
    ----------
    session : AsyncSession
        The asynchronous session for database operations.
    user_id : int
        The ID of the user to be retrieved.

    Returns
    -------
    User | None
        The user object with their followers and following relationships if a
        matching user is found, else None.
    """
    stmt = (
        select(User)
        .options(
            joinedload(User.followers),
            joinedload(User.following),
        )
        .where(User.id == user_id)
    )
    return await session.scalar(stmt)


async def get_user_following_node(
    session: AsyncSession,
    user_id: int,
    follower_id: int,
) -> Follower | None:
    """
    Retrieve a follower relationship by user ID and follower ID from the database.

    Parameters
    ----------
    session : AsyncSession
        The database session for executing operations.
    user_id : int
        The ID of the user who is being followed.
    follower_id : int
        The ID of the follower.

    Returns
    -------
    Follower or None
        The follower relationship object if found, otherwise None.
    """
    stmt = select(Follower).where(
        Follower.user_id == user_id,
        Follower.follower == follower_id,
    )
    return await session.scalar(stmt)


async def create_user_following_node(
    session: AsyncSession,
    user_id: int,
    follower_id: int,
) -> bool:
    """
    Create a follower relation between two users.

    This function establishes a relationship where the user with the given
    follower_id starts following the user with the given user_id.

    Parameters
    ----------
    session : AsyncSession
        The asynchronous session for database operations.
    follower_id : int
        The ID of the user who wants to follow another user.
    user_id : int
        The ID of the user to be followed.

    Returns
    -------
    bool
        True if the follower relationship is successfully created, False otherwise.
    """
    new_user_following_node = Follower(
        user_id=user_id,
        follower=follower_id,
    )
    session.add(new_user_following_node)
    try:
        await session.commit()
    except IntegrityError:
        return False
    return True


async def delete_user_following_node(
    session: AsyncSession,
    follower_id: int,
    user_id: int,
) -> bool:
    """
    Delete a following relationship between two users.

    This function removes the relationship where the user with the given
    follower_id stops following the user with the given user_id.
    Raises an HTTP exception if such a relationship is not found.

    Parameters
    ----------
    session : AsyncSession
        Asynchronous session for database operations.
    follower_id : int
        The ID of the user who wants to unfollow another user.
    user_id : int
        The ID of the user being unfollowed.

    Returns
    -------
    bool
        True if the following relationship was successfully deleted, False otherwise.
    """
    user_following_node = await get_user_following_node(
        session=session,
        user_id=user_id,
        follower_id=follower_id,
    )

    if not user_following_node:
        return False
    await session.delete(user_following_node)
    await session.commit()
    return True
