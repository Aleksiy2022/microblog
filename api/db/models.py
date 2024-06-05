from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """
    An abstract base class for all declarative models.

    This class doesn't define any additional fields or methods.
    It serves as a base for other SQLAlchemy models to inherit from, ensuring
    a consistent declarative base across the application.
    """


class Follower(Base):
    """
    A model representing the followers relationship between users.

    Attributes
    ----------
    tablename : str
        The name of the table in the database.
    user_id : int
        The ID of the user being followed.
    follower : int
        The ID of the follower user.
    """

    __tablename__ = "user_followers"
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    follower: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )


class User(Base):
    """
    A model representing a user in the system.

    Attributes
    ----------
    tablename : str
        The name of the table in the database.
    id : int
        The unique identifier for the user.
    name : str
        The name of the user, with a maximum length of 50 characters.
    api_key : str
        The unique API key for the user, with a maximum length of 30 characters.
    following : List[User]
        The list of users that this user is following.
    followers : List[User]
        The list of users following this user.
    tweets : List[Tweet]
        The list of tweets created by the user.
    tweet_likes : List[TweetLike]
        The list of tweet likes made by the user.
    """

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    api_key: Mapped[str] = mapped_column(String(30), unique=True)

    following: Mapped[List["User"]] = relationship(
        secondary="user_followers",
        primaryjoin="User.id==Follower.follower",
        secondaryjoin="User.id==Follower.user_id",
        lazy="noload",
        back_populates="following",
    )
    followers: Mapped[List["User"]] = relationship(
        secondary="user_followers",
        primaryjoin="User.id==Follower.user_id",
        secondaryjoin="User.id==Follower.follower",
        lazy="noload",
        back_populates="followers",
    )

    tweets: Mapped[List["Tweet"]] = relationship(
        back_populates="author",
        lazy="noload",
        cascade="all, delete-orphan",
    )
    tweet_likes: Mapped[List["TweetLike"]] = relationship(
        back_populates="user",
        lazy="noload",
        cascade="all, delete-orphan",
    )


class Tweet(Base):
    """
    A model representing a tweet posted by a user.

    Attributes
    ----------
    tablename : str
        The name of the table in the database.
    id : int
        The unique identifier for the tweet.
    content : str
        The content of the tweet, with a maximum length of 500 characters.
    created_at : datetime
        The timestamp when the tweet was created.
    user_id : int
        The ID of the user who created the tweet.
    attachments : List[Image]
        The list of images attached to the tweet.
    author : User
        The user who created the tweet.
    tweet_likes : List[TweetLike]
        The list of likes associated with the tweet.
    """

    __tablename__ = "tweets"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(
        String(500),
        default="",
        server_default="",
    )
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
    attachments: Mapped[List["Image"]] = relationship(
        lazy="noload",
        cascade="all, delete-orphan",
    )

    author: Mapped["User"] = relationship(
        back_populates="tweets",
        lazy="noload",
    )
    tweet_likes: Mapped[List["TweetLike"]] = relationship(
        back_populates="tweet",
        lazy="noload",
        cascade="all, delete-orphan",
    )


class Image(Base):
    """
    A model representing an image attached to a tweet.

    Attributes
    ----------
    tablename : str
        The name of the table in the database.
    id : int
        The unique identifier for the image.
    tweet_id : int | None
        The ID of the tweet the image is attached to; can be nullable.
    src : str
        The source URL or path of the image.
    """

    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    tweet_id: Mapped[int] = mapped_column(
        ForeignKey(
            "tweets.id",
            ondelete="CASCADE",
        ),
        nullable=True,
    )
    src: Mapped[str]


class TweetLike(Base):
    """
    A model representing a like on a tweet by a user.

    Attributes
    ----------
    tablename : str
        The name of the table in the database.
    user_id : int
        The ID of the user who liked the tweet.
    tweet_id : int
        The ID of the tweet that was liked.
    user : User
        The user who liked the tweet.
    tweet : Tweet
        The tweet that was liked.
    """

    __tablename__ = "tweet_likes"

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    tweet_id: Mapped[int] = mapped_column(
        ForeignKey(
            "tweets.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    user: Mapped["User"] = relationship(back_populates="tweet_likes")
    tweet: Mapped["Tweet"] = relationship(back_populates="tweet_likes")
