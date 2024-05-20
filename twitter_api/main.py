from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import select

from .core import db_helper
from .db import User, create_fake_data_bd
from .routers import media, tweets, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    session = db_helper.get_scoped_session()
    stmt = select(User).where(User.id == 1)
    user: User | None = await session.scalar(stmt)
    if not user:
        await create_fake_data_bd()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(users.router)
app.include_router(tweets.router)
app.include_router(media.router)
