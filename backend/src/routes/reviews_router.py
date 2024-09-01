from fastapi import Depends, APIRouter, Response

from sqlalchemy.ext.asyncio import AsyncSession

from typing import Optional

from backend.src.database.database import get_db
from backend.src.database.shema import User
from backend.src.database import shema
from backend.src.helpers.token_helper import get_token
from backend.src.repository import reviews_repository
from backend.src.repository.reviews_repository import get_all_reviews, fetch_review, fetch_filtered_review

reviews_router = APIRouter(
    prefix="/book_reviews/reviews",
    tags=["reviews"]
)


@reviews_router.get("/")
async def get_reviews(db: AsyncSession = Depends(get_db)):
    return await get_all_reviews(db=db)


@reviews_router.post("/create_review/")
async def create_review(response: Response,
                        book_name: str,
                        book_author_name: str,
                        review_title: str,
                        review_body: str,
                        db: AsyncSession = Depends(get_db),
                        token: str = Depends(get_token)):

    request = shema.Review(reviewed_book_name=book_name,
                           reviewed_book_author_name=book_author_name,
                           review_title=review_title,
                           review_body=review_body)

    return await reviews_repository.create_review(request=request, response=response, token=token, db=db)


@reviews_router.delete("/delete_review/{review_id}")
async def delete_review(review_id: int,
                        db: AsyncSession = Depends(get_db),
                        token: str = Depends(get_token)):

    return await reviews_repository.delete_review(review_id=review_id, db=db, token=token)


@reviews_router.get("/{review_id}")
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
