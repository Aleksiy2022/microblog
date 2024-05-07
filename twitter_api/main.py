from fastapi import FastAPI
from .routers import users, tweets, media


app = FastAPI()
app.include_router(users.router)
app.include_router(tweets.router)
app.include_router(media.router)
