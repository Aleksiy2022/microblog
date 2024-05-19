from pydantic import BaseModel


class UserOut(BaseModel):
    class Config:
        from_attributes = True

    id: int
    name: str


class UserWithFollowersAndFollowing(UserOut):

    followers: list[UserOut] = []
    following: list[UserOut] = []


class LikeOut(BaseModel):
    class Config:
        from_attributes = True

    user_id: int
    tweet_id: int


class ImageOut(BaseModel):

    class Config:
        from_attributes = True

    src: str


class TweetOut(BaseModel):
    class Config:
        from_attributes = True

    id: int
    content: str
    attachments: list[str] = []
    author: UserOut
    likes: list[LikeOut] = []


class UserResponse(BaseModel):
    result: bool
    user: UserWithFollowersAndFollowing


class TweetsResponse(BaseModel):
    result: bool
    tweets: list[TweetOut] = []
