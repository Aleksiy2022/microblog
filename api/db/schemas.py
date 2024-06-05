from pydantic import BaseModel


class UserOut(BaseModel):
    """
    A user output model.

    Attributes
    ----------
    id : int
        The unique identifier of the user.
    name : str
        The name of the user.
    """

    class Config:
        from_attributes = True

    id: int
    name: str


class UserWithFollowersAndFollowing(UserOut):
    """
    A user model that includes followers and following information.

    Attributes
    ----------
    followers : list[UserOut], optional
        A list of users who follow this user. Default is an empty list.
    following : list[UserOut], optional
        A list of users whom this user follows. Default is an empty list.
    """

    followers: list[UserOut] = []
    following: list[UserOut] = []


class LikeOut(BaseModel):
    """
    A like output model.

    Attributes
    ----------
    user_id : int
        The unique identifier of the user who liked the tweet.
    tweet_id : int
        The unique identifier of the tweet that was liked.
    """

    class Config:
        from_attributes = True

    user_id: int
    tweet_id: int


class ImageOut(BaseModel):
    """
    An image output model.

    Attributes
    ----------
    src : str
        The source URL of the image.
    """

    class Config:
        from_attributes = True

    src: str


class TweetOut(BaseModel):
    """
    A tweet output model.

    Attributes
    ----------
    id : int
        The unique identifier of the tweet.
    content : str
        The content of the tweet.
    attachments : list[str], optional
        A list of attachment URLs associated with the tweet. Default is an empty list.
    author : UserOut
        The author of the tweet.
    likes : list[LikeOut], optional
        A list of likes associated with the tweet. Default is an empty list.
    """

    class Config:
        from_attributes = True

    id: int
    content: str
    attachments: list[str] = []
    author: UserOut
    likes: list[LikeOut] = []


class UserResponse(BaseModel):
    """
    A response model for user-related API requests.

    Attributes
    ----------
    result : bool
        The result of the request.
    user : UserWithFollowersAndFollowing
        The user information.
    """

    result: bool
    user: UserWithFollowersAndFollowing


class TweetsResponse(BaseModel):
    """
    A response model for tweet-related API requests.

    Attributes
    ----------
    result : bool
        The result of the request.
    tweets : list[TweetOut]
        A list of tweets.
    """

    result: bool
    tweets: list[TweetOut] = []
