from sqlalchemy import Column, Integer, String, desc, func, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from database import Base


class Post(Base):
    pass


class User(Base):
    __tablename__ = 'user'
    id = 
    gender = 
    age = 
    country = 
    city = 
    exp_group = 
    os = 
    source = 
    pass


class Feed(Base):
    __tablename__ = 'feed_action'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user = relationship(User)
    post_id = Column(Integer, ForeignKey('post.id'), primary_key=True)
    post = relationship(Post)
    action = Column(String)
    time = Column(TIMESTAMP)
