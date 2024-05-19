from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from typing import List


class Base(DeclarativeBase):
    pass


class Follower(Base):
    __tablename__ = "user_followers"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    follower: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    api_key: Mapped[str] = mapped_column(unique=True)

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
    __tablename__ = "tweets"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(
        String(500),
        default="",
        server_default="",
    )
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
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweets.id", ondelete="CASCADE",), nullable=True)
    src: Mapped[str]


class TweetLike(Base):
    __tablename__ = "tweet_likes"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweets.id", ondelete="CASCADE"), primary_key=True)

    user: Mapped["User"] = relationship(back_populates="tweet_likes")
    tweet: Mapped["Tweet"] = relationship(back_populates="tweet_likes")
