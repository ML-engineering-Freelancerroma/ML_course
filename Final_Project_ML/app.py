from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

# from schema import UserGet, PostGet, FeedGet
# from table_post import Post
# from table_user import User
# from table_feed import Feed
from database import SessionLocal


app = FastAPI()


def get_db():
    with SessionLocal() as db:
        return db


@app.get('/user/{id}', response_model=UserGet)
def user_get(id: int, db: Session = Depends(get_db)):
    response = db.query(User).filter(User.id == id).one_or_none()
    if response is None:
        raise HTTPException(404, f'No user with id {id}')
    return response


@app.get('/post/{id}', response_model=PostGet)
def post_get(id: int, db: Session = Depends(get_db)):
    response = db.query(Post).filter(Post.id == id).one_or_none()
    if response is None:
        raise HTTPException(404, f'No post with id {id}')
    return response


@app.get('/user/{id}/feed', response_model=List[FeedGet])
def feed_user_get(id: int, limit=10, db: Session = Depends(get_db)):
    response = db.query(Feed).filter(Feed.user_id == id).order_by(desc(Feed.time)).limit(limit).all()
    return response


@app.get('/post/{id}/feed', response_model=List[FeedGet])
def feed_user_get(id: int, limit=10, db: Session = Depends(get_db)):
    response = db.query(Feed).filter(Feed.post_id == id).order_by(desc(Feed.time)).limit(limit).all()
    return response


@app.get('/post/recommendations/', response_model=List[PostGet])
def get_recommended_feed(id: int, limit=10, db: Session = Depends(get_db)) -> List[PostGet]:
    response = (
        db.query(Post.id, Post.text, Post.topic).
        select_from(Feed).
        join(Post, Post.id == Feed.post_id).
        filter(Feed.action == 'like').
        group_by(Post.id).
        order_by(func.count(Feed.post_id).desc()).
        limit(limit).
        all()
    )
    return response
