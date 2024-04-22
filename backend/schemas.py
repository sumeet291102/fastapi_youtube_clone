from pydantic import BaseModel
from datetime import datetime


class LikeBase(BaseModel):
    created_at: datetime = datetime.now()


class LikeCreate(LikeBase):
    pass


class Like(LikeBase):
    id: int
    liked_on_id: int
    liked_by_id: int

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    content: str
    created_at: datetime = datetime.now()


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    commented_on_id: int
    commented_by_id: int

    class Config:
        orm_mode = True


class SubscriberBase(BaseModel):
    created_at: datetime = datetime.now()


class SubscriberCreate(SubscriberBase):
    pass


class Subscriber(SubscriberBase):
    subscriber_id: int
    subscribee_id: int

    class Config:
        orm_mode = True


class VideoBase(BaseModel):
    title: str
    description: str
    created_at: datetime = datetime.now()
    url: str


class VideoCreate(VideoBase):
    pass


class Video(VideoBase):
    id: int
    uploaded_by_id: int
    likes: list[Like] = []
    comments: list[Comment] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    profile_pic: str | None = None
    profile_cover: str | None = None
    user_description: str | None = None
    created_at: datetime = datetime.now()


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    videos: list[Video] = []
    comments: list[Comment] = []
    likes: list[Like] = []

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    profile_pic: str | None = None
    profile_cover: str | None = None
    user_description: str | None = None
    username: str
