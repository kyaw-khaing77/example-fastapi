import json
from pydantic import BaseModel, EmailStr, model_validator
import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class User(UserBase):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    user_id: int
    created_at: datetime.datetime
    votes: int

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


class VoteCreate(BaseModel):
    post_id: int
    dir: int  # 1 = vote, 0 = remove vote

    @model_validator(mode="before")
    @classmethod
    def parse_string_input(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v
