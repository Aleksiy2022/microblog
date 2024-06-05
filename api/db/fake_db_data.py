import factory  # type: ignore
from async_factory_boy.factory.sqlalchemy import AsyncSQLAlchemyFactory  # type: ignore

from ..core import db_helper
from .models import Base, Tweet, User


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
        sqlalchemy_session = db_helper.sc_session

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
        sqlalchemy_session = db_helper.sc_session

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
        sqlalchemy_session = db_helper.sc_session
        sqlalchemy_session_persistence = "commit"

    content = factory.Faker("text")
    user_id = factory.Sequence(lambda id_num: f"user_id{id_num}")


async def create_fake_data_bd() -> None:
    """
    Asynchronously create fake data in the database.

    Connects to the database and creates all defined tables. Subsequently,
    creates one test user and a batch of five users. For each created user,
    it generates and stores a tweet associated with the user.
    """
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await TestUser.create()
    users = await UserFactory.create_batch(5)
    for user in users:
        await TweetFactory.create(user_id=user.id)
