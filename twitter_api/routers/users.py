from typing import Annotated

from fastapi import APIRouter, Depends, Path, Request
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
    print("*********************")
    print(current_user)
    print(current_user.id)
    user = await users_qr.get_user_by_id(
        session,
        user_id=current_user.id,
    )
    if user:
        return {
            "result": True,
            "user": user,
        }


@router.api_route("/{id}/follow", methods=["POST", "DELETE"])
async def user_following_node(
    id: int,
    request: Request,
    current_user: Annotated[
        schemas.UserOut, Depends(get_current_user_by_api_key)
    ],
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
):
    if request.method == "POST":
        if await users_qr.create_user_following_node(
            session,
            follower_id=current_user.id,
            user_id=id,
        ):
            return {
                "result": True,
            }
    elif request.method == "DELETE":
        if await users_qr.delete_user_following_node(
            session,
            follower_id=current_user.id,
            user_id=id,
        ):
            return {
                "result": True,
            }


@router.get("/{id}", response_model=schemas.UserResponse)
async def user_profile(
    id: Annotated[int, Path(ge=1)],
    session: Annotated[AsyncSession, Depends(scoped_session_db)],
):
    user = await users_qr.get_user_by_id(session, user_id=id)
    if user:
        return {
            "result": True,
            "user": user,
        }
