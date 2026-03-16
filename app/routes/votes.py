from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.models.vote import Vote as VoteModel
from app.models.post import Post as PostModel
from app.routes.oauth import get_current_user

router = APIRouter(prefix="/vote", tags=["votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.VoteCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    # Check post exists
    post = db.query(PostModel).filter(PostModel.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    existing_vote = db.query(VoteModel).filter(
        VoteModel.post_id == vote.post_id,
        VoteModel.user_id == current_user.id
    ).first()

    if vote.dir == 1:
        if existing_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already voted on this post")
        new_vote = VoteModel(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added"}
    else:
        if not existing_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found")
        db.delete(existing_vote)
        db.commit()
        return {"message": "Vote removed"}
