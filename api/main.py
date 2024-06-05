from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import select

from .core import db_helper, settings
from .db import User, create_fake_data_bd
from .routers import media, tweets, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Asynchronous context manager.

    It can be removed or changed. This function is designed to fill the
    database with fake data.

    Parameters
    ----------
    app : FastAPI
        The FastAPI application instance.

    Yields
    ------
    None
        Provides control back to the application.

    """
    session = db_helper.get_scoped_session()
    stmt = select(User).where(User.id == 1)
    user: User | None = await session.scalar(stmt)
    await session.close()
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
                    },
                },
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
                    },
                },
            },
        },
    },
)


app.include_router(users.router)
app.include_router(tweets.router)
app.include_router(media.router)


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """
    Exception handler for HTTPException in FastAPI applications.

    This function intercepts HTTPException errors and returns a JSONResponse
    with a standardized error format. It ensures that the API provides
    informative error messages to the client.

    Parameters
    ----------
    request : Request
        The incoming HTTP request.
    exc : HTTPException
        The HTTPException raised during request processing.

    Returns
    -------
    JSONResponse
        A response object with a status code and a JSON body containing error details.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            {
                "result": False,
                "error_type": type(exc).__name__,
                "error_message": exc.detail,
            },
        ),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    """
    Exception handler for RequestValidationError in FastAPI applications.

    This function handles validation errors raised during request processing,
    returning a JSON response with a standardized error format. It ensures that
    clients receive clear and useful information about validation issues.

    Parameters
    ----------
    request : Request
        The incoming HTTP request.
    exc : RequestValidationError
        The validation error raised during request processing.

    Returns
    -------
    JSONResponse
        A response object with a 422 status code and a JSON body containing error details.
    """
    error_message = exc.errors()[0]
    error_type = error_message.get("type")
    error_msg = error_message.get("msg")
    if exc.body:
        error_message = exc.body
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(
            {
                "result": False,
                "error_type": error_type,
                "error_message": error_msg,
            },
        ),
    )


@app.middleware("http")
async def max_upload_size(request: Request, call_next):
    """
    Middleware to enforce maximum upload size in FastAPI applications.

    This middleware checks if the incoming request contains a file that exceeds
    the allowable size limit (1MB). If the file is too large, it returns a JSON
    response with a 413 status code and an appropriate error message.

    Parameters
    ----------
    request : Request
        The incoming HTTP request.
    call_next : function
        The next middleware or endpoint to be called if the request passes the size check.

    Returns
    -------
    JSONResponse or Response
        A response object, either with a 413 status code and error details if the file
        is too large, or the response from the next middleware/endpoint if the file size
        is within the acceptable limit.

    """
    try:
        if is_file_too_large(request):
            return JSONResponse(
                status_code=413,
                content={
                    "result": False,
                    "error_type": "error max size",
                    "error_message": "File too large. Maximum allowed size is 1MB",
                },
            )
    except (ValueError, KeyError):
        pass
    return await call_next(request)


def is_file_too_large(request: Request) -> bool:
    """
    Check if the uploaded file in the request exceeds the maximum allowable size.

    This function inspects the 'Content-Type' and 'Content-Length' headers of the incoming request
    to determine if it contains a file that is too large. It specifically checks for files
    submitted through multipart/form-data encoding.

    Parameters
    ----------
    request : Request
        The incoming HTTP request containing the file upload.

    Returns
    -------
    bool
        True if the file exceeds the maximum allowable size, False otherwise.
    """
    content_type = request.headers.get("content-type")
    content_length = request.headers.get("content-length")

    is_multipart = content_type and "multipart/form-data" in content_type
    if is_multipart and content_length:
        return int(content_length) > settings.max_file_size_bytes
    return False
