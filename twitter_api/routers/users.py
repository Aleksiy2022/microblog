from typing import Annotated

from fastapi import APIRouter, Depends, Path
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import schemas, users_qr
from ..dependencies import get_current_user_by_api_key, scoped_session_db

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)


@router.get("/me", response_model=schemas.UserResponse)
async def current_user_profile(
    current_user: Annotated[
        schemas.UserOut, Depends(get_current_user_by_api_key)
    ],
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
):
    user = await users_qr.get_user_by_id(
        session,
        user_id=current_user.id,
    )
    if user:
        return {
            "result": True,
            "user": user,
        }
    else:
        raise HTTPException(
            status_code=404, detail=f"User with id: {id} not found"
        )


@router.post("/{id}/follow")
async def create_user_following_node(
    id: Annotated[int, Path(ge=1, le=9999999)],
    current_user: Annotated[
        schemas.UserOut, Depends(get_current_user_by_api_key)
    ],
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
):
    if await users_qr.create_user_following_node(
        session,
        follower_id=current_user.id,
        user_id=id,
    ):
        return {"result": True}


@router.delete("/{id}/follow")
async def delete_user_following_node(
    id: Annotated[int, Path(ge=1, le=9999999)],
    current_user: Annotated[
        schemas.UserOut, Depends(get_current_user_by_api_key)
    ],
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
):
    if await users_qr.delete_user_following_node(
        session,
        follower_id=current_user.id,
        user_id=id,
    ):
        return {"result": True}


@router.get("/{id}", response_model=schemas.UserResponse)
async def user_profile(
    id: Annotated[int, Path(ge=1, le=9999999)],
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
):
    user = await users_qr.get_user_by_id(session, user_id=id)
    if user:
        return {
            "result": True,
            "user": user,
        }
    else:
        raise HTTPException(
            status_code=404, detail=f"User with id: {id} not found"
        )
