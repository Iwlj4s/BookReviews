from fastapi import Depends, APIRouter, Response

from sqlalchemy.ext.asyncio import AsyncSession

from typing import Optional

from backend.src.database.database import get_db
from backend.src.database.shema import User
from backend.src.database import shema
from backend.src.helpers.token_helper import get_token
from backend.src.repository.reviews_repository import get_all_reviews, fetch_review, fetch_filtered_review

reviews_router = APIRouter(
    prefix="/book_reviews/reviews",
    tags=["reviews"]
)


@reviews_router.get("/")
async def get_reviews(db: AsyncSession = Depends(get_db)):
    return await get_all_reviews(db=db)


@reviews_router.get("/reviews/{review_id}")
async def get_review(review_id: int, response: Response, db: AsyncSession = Depends(get_db)):
    return await fetch_review(review_id=review_id, response=response, db=db)


@reviews_router.get("/filtered/")
async def get_filtered_review(response: Response,
                              book_name: str | None = None,
                              author_name: str | None = None,
                              db: AsyncSession = Depends(get_db)):
    request = shema.FilteredReview(reviewed_book_name=book_name,
                                   reviewed_author_name=author_name)

    return await fetch_filtered_review(request=request, response=response, db=db)
