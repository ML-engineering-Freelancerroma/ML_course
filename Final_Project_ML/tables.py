from sqlalchemy import (
    Column,
    Integer,
    String,
    desc,
    func,
    ForeignKey,
    TIMESTAMP
)
from sqlalchemy.orm import relationship

from database import Base


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    topic = Column(String)    


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    gender = Column(Integer)
    age = Column(Integer)
    country = Column(String)
    city = Column(String)
    exp_group = Column(Integer)
    os = Column(String)
    source = Column(String)


class Feed(Base):
    __tablename__ = 'feed_action'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user = relationship(User)
    post_id = Column(Integer, ForeignKey('post.id'), primary_key=True)
    post = relationship(Post)
    action = Column(String)
    time = Column(TIMESTAMP)


