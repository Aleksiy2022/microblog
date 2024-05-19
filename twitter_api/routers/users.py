from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import users_qr, schemas
from ..dependencies import get_api_key, scoped_session_db
from typing import Annotated

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)


@router.get("/me", response_model=schemas.UserResponse)
async def get_user_by_api_key(
        api_key: str = Depends(get_api_key),
        session: AsyncSession = Depends(scoped_session_db)
):
    user = await users_qr.get_user_by_api_key(session, api_key=api_key)
    return {
        "result": True,
        "user": user
    }


@router.get("/{id}", response_model=schemas.UserResponse)
async def get_user(
        id: Annotated[int, Path(ge=1)],
        session: AsyncSession = Depends(scoped_session_db),
):
    user = await users_qr.get_user_by_id(session, user_id=id)
    return {
        "result": True,
        "user": user
    }
