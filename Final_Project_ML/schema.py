from datetime import datetime

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
