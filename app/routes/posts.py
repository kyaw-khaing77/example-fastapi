from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session

from app.models.post import Post as PostModel
from app.models.vote import Vote as VoteModel
from app import schemas
from app.database import get_db
from app.routes.oauth import get_current_user

router = APIRouter(prefix="/posts", tags=["posts"])


# GET all posts
@router.get("/", response_model=List[schemas.Post])
def get_all_posts(db: Session = Depends(get_db) , current_user: str = Depends(get_current_user)):
    posts = db.query(PostModel).all()
    result = []
    for post in posts:
        votes = db.query(VoteModel).filter(VoteModel.post_id == post.id).count()
        post_data = post.__dict__.copy()
        post_data["votes"] = votes
        result.append(post_data)
    return result


# GET single post by ID
@router.get("/{post_id}", response_model=schemas.Post)
def get_post(post_id: int, db: Session = Depends(get_db) , current_user: str = Depends(get_current_user)):
    post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    votes = db.query(VoteModel).filter(VoteModel.post_id == post.id).count()
    post_data = post.__dict__.copy()
    post_data["votes"] = votes
    return post_data


# CREATE post
@router.post("/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_post = PostModel(**post.dict(), user_id=current_user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    post_data = db_post.__dict__.copy()
    post_data["votes"] = 0
    return post_data


# UPDATE post
@router.put("/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    for key, value in post.dict().items():
        setattr(db_post, key, value)
    db.commit()
    db.refresh(db_post)
    votes = db.query(VoteModel).filter(VoteModel.post_id == db_post.id).count()
    post_data = db_post.__dict__.copy()
    post_data["votes"] = votes
    return post_data


# DELETE post
@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    votes = db.query(VoteModel).filter(VoteModel.post_id == db_post.id).count()
    post_data = db_post.__dict__.copy()
    post_data["votes"] = votes
    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted", "deleted_post": post_data}
