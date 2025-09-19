from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from schema import UserGet, PostGet, FeedGet
from tables import Post, User, Feed
from database import SessionLocal
from service import (
    predict_posts, predict_test_posts, load_post_texts, get_exp_group
)


app = FastAPI()


def get_db():
    with SessionLocal() as db:
        yield db


@app.get('/user/{id}', response_model=UserGet)
def user_get(
    id: int,
    db: Session = Depends(get_db)
) -> User:
    response = (
        db.query(User).
        filter(User.id == id).
        one_or_none()
    )
    if response is None:
        raise HTTPException(404, f'No user with id {id}')
    return response


@app.get('/post/{id}', response_model=PostGet)
def post_get(
    id: int,
    db: Session = Depends(get_db)
) -> Post:
    response = (
        db.query(Post).
        filter(Post.id == id).
        one_or_none()
    )
    if response is None:
        raise HTTPException(404, f'No post with id {id}')
    return response


@app.get('/user/{id}/feed', response_model=List[FeedGet])
def feed_user_get(
    id: int,
    limit=10,
    db: Session = Depends(get_db)
) -> List[Feed]:
    response = (
        db.query(Feed).
        filter(Feed.user_id == id).
        order_by(desc(Feed.time)).
        limit(limit).
        all()
    )
    return response


@app.get('/post/{id}/feed', response_model=List[FeedGet])
def feed_post_get(
    id: int,
    limit=10,
    db: Session = Depends(get_db)
) -> List[Feed]:
    response = (
        db.query(Feed).
        filter(Feed.post_id == id).
        order_by(desc(Feed.time)).
        limit(limit).
        all()
    )
    return response


@app.get("/post/recommendations/", response_model=List[PostGet])
def recommended_posts(
        id: int, 
        # time: datetime, 
        limit: int = 5) -> List[PostGet]:
    post_ids = predict_posts(id, limit)
    records = load_post_texts(post_ids)

    posts = []
    for rec in records:
        rec["id"] = rec.pop("post_id")  # change "post_id" to "id"
        try:
            posts.append(PostGet(**rec))
    #     except pydantic.error_wrappers.ValidationError as e:
    #         print(f"Validation error for record {rec}: {e}")
    # return posts
