import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta ,timezone

from sqlalchemy.orm import Session
from app import schemas
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, HTTPException, Depends , status ,Response
from app.models.user import User as UserModel

from app.database import get_db
from app.config import Settings

settings = Settings()

SECRET_KEY = settings.SECRET_KEY  # In production, use a secure method to store this
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    # In production, add an expiration time to the token
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str , credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError:
        raise credentials_exception
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_token(token, credentials_exception)
    if payload is None:
        raise credentials_exception
    
    user = db.query(UserModel).filter(UserModel.email == payload.get("sub")).first()
    if user is None:
        raise credentials_exception
    return user