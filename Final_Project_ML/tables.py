from sqlalchemy import Column, Integer, String, desc, func, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from database import Base


class Feed(Base):
    __tablename__ = 'feed_action'
    user_id =
    user =
    post_id =
    post = 
    action = 
    time = Column(TIMESTAMP)