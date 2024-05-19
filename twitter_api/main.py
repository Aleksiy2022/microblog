from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routers import users, tweets, media
from .db import create_fake_data_bd
from sqlalchemy import select
from .db import User
from .core import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    session = db_helper.get_scoped_session()
    stmt = select(User).where(User.id == 1)
    user: User | None = await session.scalar(stmt)
    if not user:
        print('Создаем базу данных')
        await create_fake_data_bd()
        print("БД создана")
    else:
        print("БД уже заполнена")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(users.router)
app.include_router(tweets.router)
app.include_router(media.router)
