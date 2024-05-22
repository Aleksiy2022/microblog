from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
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


app = FastAPI(
    lifespan=lifespan,
    responses={
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "result": False,
                        "error_type": "string",
                        "error_message": "string",
                    }
                }
            },
        },
        404: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "result": False,
                        "error_type": "string",
                        "error_message": "string",
                    }
                }
            },
        },
    },
)


app.include_router(users.router)
app.include_router(tweets.router)
app.include_router(media.router)


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            {
                "result": False,
                "error_type": type(exc).__name__,
                "error_message": exc.detail,
            }
        ),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    error_message: dict = exc.errors()[0]
    error_type: dict = error_message.get("type")
    error_msg: dict = error_message.get("msg")
    print(error_message)
    if exc.body:
        error_message = exc.body
        print(error_message)
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(
            {
                "result": False,
                "error_type": error_type,
                "error_message": error_msg,
            }
        ),
    )


@app.middleware("http")
async def max_upload_size(request: Request, call_next):
    try:
        print("***********")
        print(request.headers['content-type'])
        if "multipart/form-data" in request.headers['content-type']:
            if int(request.headers["content-length"]) > 5 * 1024:
                return JSONResponse(
                    status_code=413,
                    content=jsonable_encoder(
                        {
                            "result": False,
                            "error_type": "error max size",
                            "error_message": "File too large. Maximum allowed size is 1MB",
                        }
                    ),
                )
    except KeyError:
        pass
    response = await call_next(request)
    return response
