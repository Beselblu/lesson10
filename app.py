from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from database import SessionLocal
from table_post import Post, User, Feed_Action
from schemas import UserGet, PostGet, FeedGet

app = FastAPI()


def get_db() -> Session:
    with SessionLocal() as db:
        return db


def get_user_from_id(id: int, db: Session) -> User:
    return db.query(User).filter(User.id == id).one_or_none()


def get_post_from_id(id: int, db: Session) -> Post:
    return db.query(Post).filter(Post.id == id).limit(limit).one_or_none()


def get_feed(db: Session, id:int, limit: int, by_user_id: bool) -> Feed_Action:
    return (
        db.query(Feed_Action)
        .filter(Feed_Action.user_id == id) if by_user_id else tmp.filter(Feed_Action.post_id == id)
        .order_by(desc(Feed_Action.time))
        .limit(limit)
        .all()
    )


def get_recommended_feed(db: Session, id: int, limit: int) -> Post:
    return (
        db.query(Post)
            .select_from(Feed_Action)
            .filter(Feed_Action.action == 'like')
            .join(Post)
            .group_by(Post.id)
            .order_by(desc(func.count(Post.id)))
            .limit(limit)
            .all()
    )


@app.get("/user/{id}", response_model=UserGet)
def get_all_users(id: int, db: Session = Depends(get_db)):
    user = get_user_from_id(id, db)
    
    if user is None:
        raise HTTPException(404, "user not found")
    return user


@app.get("/post/{id}", response_model=PostGet)
def get_all_post(id: int, db: Session = Depends(get_db)):
    post = get_post_from_id(id, db)

    if post is None:
        raise HTTPException(404, "post not found")
    return post


@app.get("/user/{id}/feed", response_model=List[FeedGet])
def handle_get_feed(
    id: int, 
    limit: int = 10, 
    db: Session = Depends(get_db)
) -> List[FeedGet]:
    return get_feed(db, id, limit, by_user_id=True)


@app.get("/post/{id}/feed", response_model=List[FeedGet])
def handle_get_feed(
    id: int, 
    limit: int = 10, 
    db: Session = Depends(get_db)
) -> List[FeedGet]:
    return get_feed(db, id, limit, by_user_id=False)


@app.get("/post/recommendation/", response_model=List[PostGet])
def recommended_posts(
    id: int, limit: int = 10, db: Session = Depends(get_db)
) -> List[PostGet]:
    return get_recommended_feed(db, id, limit)