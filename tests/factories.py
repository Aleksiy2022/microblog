import factory  # type: ignore
from async_factory_boy.factory.sqlalchemy import (  # type: ignore
    AsyncSQLAlchemyFactory,
)

from twitter_api.core import test_db_helper
from twitter_api.db import Base, Tweet, User


class TestUser(AsyncSQLAlchemyFactory):
    class Meta:
        model = User
        sqlalchemy_session = test_db_helper.sc_session

    name = "Aleksiy"
    api_key = "test"


class UserFactory(AsyncSQLAlchemyFactory):
    class Meta:
        model = User
        sqlalchemy_session = test_db_helper.sc_session

    name = factory.Faker("first_name")
    api_key = factory.Faker("ean")


class TweetFactory(AsyncSQLAlchemyFactory):
    class Meta:
        model = Tweet
        sqlalchemy_get_or_create = ("user_id",)
        sqlalchemy_session = test_db_helper.sc_session
        sqlalchemy_session_persistence = "commit"

    content = factory.Faker("text")
    user_id = factory.Sequence(lambda n: "user_id%s" % n)


async def create_fake_data_bd():
    async with test_db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await TestUser.create()
    users = await UserFactory.create_batch(5)
    for user in users:
        await TweetFactory.create(user_id=user.id)
