import uvicorn
from fastapi import FastAPI

from routers import users, tweets, media
from db import database, models

app = FastAPI()
app.include_router(users.router)
app.include_router(tweets.router)
app.include_router(media.router)


# async def init_db():
#     async with database.db_helper.engine.begin() as conn:
#         await conn.run_sync(models.Base.metadata.create_all)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
