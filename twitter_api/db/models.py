from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    api_key: Mapped[str] = mapped_column(unique=True, nullable=False)

    tweets: Mapped[List["Tweet"]] = relationship(back_populates="author")
    likes: Mapped[List["Like"]] = relationship(back_populates="user")
    following: Mapped[List["User"]] = relationship(
        "User",
        secondary="UserFollowing",
        primaryjoin="User.id == UserFollowing.user_id",
        secondaryjoin="User.id == UserFollowing.following_id",
        backref="followers",
    )


class UserFollowing(Base):
    __tablename__ = "user_following"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    following_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)


class Tweet(Base):
    __tablename__ = "tweets"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str]
    author: Mapped["User"] = mapped_column(ForeignKey("users.id"))
    attachments: Mapped[List["Image"]] = relationship()

    likes: Mapped[List["Like"]] = relationship(back_populates="tweet")


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweets.id"))
    src: Mapped[str]


class Like(Base):
    __tablename__ = "likes"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweets.id"), primary_key=True)

    user: Mapped["User"] = relationship(back_populates="likes")
    tweet: Mapped["Tweet"] = relationship(back_populates="likes")
