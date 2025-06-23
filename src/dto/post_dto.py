from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PostCreateDTO(BaseModel):
    text: str = Field(..., min_length=5, max_length=30)
    user_id: int
    reply_to_id: Optional[int] = Field(None, gt=0)


class PostFilterDTO(BaseModel):
    search: Optional[str]
    owner_id: Optional[int]
    user_id: Optional[int] = Field(None, gt=0)
    reply_to_id: Optional[int] = Field(None, gt=0)
    limit: Optional[int] = Field(None, gt=0)
    offset: Optional[int] = Field(None, ge=0)


class PostReadDTO(BaseModel):
    id: int
    text: str
    created_at: datetime
    reply_to_id: Optional[int]


class PostUserDTO(BaseModel):
    id: int
    user_name: str
    first_name: Optional[str]
    last_name: Optional[str]


class DetailedPostReadDTO(BaseModel):
    id: int
    text: str
    created_at: datetime
    reply_to_id: Optional[int]
    likes_count: int
    views_count: int
    replies_count: int
    user_liked: bool
    user_viewed: bool
    user: PostUserDTO