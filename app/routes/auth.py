from fastapi import APIRouter, HTTPException, Depends , status ,Response
from sqlalchemy.orm import Session
from app import schemas
from app.models.user import User as UserModel
from app.database import get_db
from app.routes.users import verify_password 
from app.routes.oauth import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["auth"])

@router.post("/login" , response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # For simplicity, we return a dummy token. In production, use JWT or similar.

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}