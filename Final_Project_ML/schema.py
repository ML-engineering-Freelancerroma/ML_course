from datetime import datetime
from typing import List

from pydantic import BaseModel


class UserGet(BaseModel):
    id: int
    gender: int
    age: int
    country: str
    city: str
    exp_group: int
    os: str
    source: str

    class Config:
        from_attributes = True


class PostGet(BaseModel):
    id: int
    text: str
    topic: str

    class Config:
        from_attributes = True


class FeedGet(BaseModel):
    user_id: int
    user: UserGet
    post_id: int
    post: PostGet
    action: str
    time: datetime

    class Config:
        from_attributes = True


class Response(BaseModel):
    exp_group: str
    recommendations: List[PostGet]
