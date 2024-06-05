import factory  # type: ignore
from async_factory_boy.factory.sqlalchemy import AsyncSQLAlchemyFactory  # type: ignore

from api.core import test_db_helper
from api.db import Tweet, TweetLike, User


class TestUser(AsyncSQLAlchemyFactory):
    """
    Data factory class for generating User instances.

    This class provides a factory for creating instances of the User model
    with predefined attributes. It uses asynchronous SQLAlchemy sessions
    to interact with the database.

    Attributes
    ----------
    Meta : class
        Contains metadata for the factory such as the model and session.
    name : str
        Default name attribute for the User instance.
    api_key : str
        Default API key attribute for the User instance.
    """

    class Meta:
        model = User
        sqlalchemy_session = test_db_helper.sc_session

    name = "Aleksiy"
    api_key = "test"


class UserFactory(AsyncSQLAlchemyFactory):
    """
    Data factory class for generating User instances.

    This class provides a factory for creating instances of the User model
    with dynamically generated attributes using Faker. It uses asynchronous
    SQLAlchemy sessions to interact with the database.

    Attributes
    ----------
    Meta : class
        Contains metadata for the factory such as the model and session.
    name : str
        Dynamically generated first name attribute for the User instance.
    api_key : str
        Dynamically generated API key attribute for the User instance.
    """

    class Meta:
        model = User
        sqlalchemy_session = test_db_helper.sc_session

    name = factory.Faker("first_name")
    api_key = factory.Faker("ean")


class TweetFactory(AsyncSQLAlchemyFactory):
    """
    Factory for creating Tweet objects using SQLAlchemy and async_factory_boy.

    Attributes
    ----------
    content : str
        The content of the tweet, generated using Faker to produce random text.
    user_id : str
        A unique identifier for the user, generated sequentially.

    Meta
    ----
    model : class
        The SQLAlchemy model class to be instantiated, in this case, Tweet.
    sqlalchemy_get_or_create : tuple
        Attributes that define uniqueness for get_or_create operations, here it is ("user_id",).
    sqlalchemy_session : SQLAlchemy session
        The SQLAlchemy session used for database operations.
    sqlalchemy_session_persistence : str
        The session persistence setting, determines whether to commit the session after creating
        an object. Options are "commit" or "flush".

    Methods
    -------
    No additional methods.
    """

    class Meta:
        model = Tweet
        sqlalchemy_get_or_create = ("user_id",)
        sqlalchemy_session = test_db_helper.sc_session
        sqlalchemy_session_persistence = "commit"

    content = factory.Faker("text")
    user_id = factory.Sequence(lambda id_num: f"user_id{id_num}")


class TweetLikeFactory(AsyncSQLAlchemyFactory):
    class Meta:
        model = TweetLike
        sqlalchemy_session = test_db_helper.sc_session

    user_id = 1
    tweet_id = 2


async def create_test_data_bd():
    await TestUser.create()
    users = await UserFactory.create_batch(5)

    await TweetFactory.create(user_id=1)

    for user in users:
        await TweetFactory.create(user_id=user.id)

    await TweetLikeFactory.create()
