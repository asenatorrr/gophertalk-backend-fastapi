from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Path, status

from services.post_service import (
    get_all_posts,
    create_post,
    delete_post,
    view_post,
    like_post,
    dislike_post,
)
from dto.post_dto import DetailedPostReadDTO, PostCreateDTO, PostReadDTO, PostFilterDTO
from dependencies.auth import get_current_user, TokenPayload


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[DetailedPostReadDTO])
def get_all_posts_handler(
    limit: int = Query(10, gt=0),
    offset: int = Query(0, ge=0),
    reply_to_id: int = Query(None, gt=0),
    owner_id: int = Query(0),
    search: str = Query(""),
    user: TokenPayload = Depends(get_current_user),
):
    try:
        filter_dto = PostFilterDTO(
            user_id=user.sub,
            limit=limit,
            offset=offset,
            reply_to_id=reply_to_id,
            owner_id=owner_id,
            search=search,
        )
        return get_all_posts(filter_dto.model_dump())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/", response_model=PostReadDTO, status_code=status.HTTP_201_CREATED)
def create_post_handler(dto: PostCreateDTO, user: TokenPayload = Depends(get_current_user)):
    try:
        dto.user_id = user.sub
        return create_post(dto.model_dump())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_handler(post_id: int = Path(..., gt=0), user: TokenPayload = Depends(get_current_user)):
    try:
        delete_post(post_id, user.sub)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{post_id}/view", status_code=status.HTTP_201_CREATED)
def view_post_handler(post_id: int = Path(..., gt=0), user: TokenPayload = Depends(get_current_user)):
    try:
        view_post(post_id, user.sub)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{post_id}/like", status_code=status.HTTP_201_CREATED)
def like_post_handler(post_id: int = Path(..., gt=0), user: TokenPayload = Depends(get_current_user)):
    try:
        like_post(post_id, user.sub)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{post_id}/like", status_code=status.HTTP_204_NO_CONTENT)
def dislike_post_handler(post_id: int = Path(..., gt=0), user: TokenPayload = Depends(get_current_user)):
    try:
        dislike_post(post_id, user.sub)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
