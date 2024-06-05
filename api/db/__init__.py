"""
Package 'db_queries'.

1. The 'db_queries' package contains modules that provide interaction with the
database (CRUD operations with the database).
2. The 'fake_db_data' module initializes fake data for demonstrating the
microblog's functionality.
3. The 'models' module - models for creating database tables.
4. The 'schemas' module - contains schemas that help describe the data models
that the application expects as input and returns as output.
"""

__all__ = (
    "Base",
    "User",
    "Tweet",
    "Image",
    "TweetLike",
    "UserFactory",
    "create_fake_data_bd",
    "tweets_qr",
    "users_qr",
    "medias_qr",
    "likes_qr",
    "TestUser",
    "TweetFactory",
    "UserOut",
)

from .db_queries import likes_qr, medias_qr, tweets_qr, users_qr
from .fake_db_data import TestUser, TweetFactory, UserFactory, create_fake_data_bd
from .models import Base, Image, Tweet, TweetLike, User
from .schemas import UserOut
