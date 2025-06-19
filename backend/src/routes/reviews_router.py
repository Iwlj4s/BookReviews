from typing import List

from fastapi import Depends, APIRouter, Response

from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database.database import get_db
from backend.src.database.shema import User, ReviewCreate
from backend.src.database import shema, models
from backend.src.repository.admin_repository import get_current_admin_user

from backend.src.repository.user_repository import get_current_user
from backend.src.repository import reviews_repository
from backend.src.repository.reviews_repository import get_all_reviews, fetch_review, fetch_filtered_review

reviews_router = APIRouter(
    prefix="/book_reviews/api/reviews",
    tags=["reviews"]
)


@reviews_router.get("/", tags=["reviews"], response_model=List[shema.ReviewOut])
async def get_reviews(db: AsyncSession = Depends(get_db)):
    return await get_all_reviews(db=db)


@reviews_router.post("/create_review/", tags=["reviews"])
async def create_review(response: Response,
                        request: ReviewCreate,
                        db: AsyncSession = Depends(get_db),
                        user: User = Depends(get_current_user)):
    print("Request from back: ", request)
    new_review = await reviews_repository.create_review(request=request,
                                                        response=response,
                                                        user=user,
                                                        db=db)
    return new_review


@reviews_router.put("/change_review/{review_id}", tags=["reviews"])
async def change_review(review_id: int,
                        request: shema.ChangeReview,
                        db: AsyncSession = Depends(get_db),
                        user: User = Depends(get_current_user) or Depends(get_current_admin_user)):
    return await reviews_repository.change_review(review_id=int(review_id),
                                                  request=request,
                                                  db=db,
                                                  user=user)


@reviews_router.delete("/delete_review/{review_id}", tags=["reviews"])
async def delete_review(review_id: int,
                        db: AsyncSession = Depends(get_db),
                        user: User = Depends(get_current_user)):
    return await reviews_repository.delete_review(review_id=review_id, db=db)


@reviews_router.get("/{review_id}", tags=["reviews"], response_model=shema.Review)
async def get_review(review_id: int, response: Response, db: AsyncSession = Depends(get_db)):
    return await fetch_review(review_id=review_id, response=response, db=db)


@reviews_router.get("/filtered/", tags=["reviews"], response_model=List[shema.Review])
async def get_filtered_review(response: Response,
                              book_name: str | None = None,
                              author_name: str | None = None,
                              db: AsyncSession = Depends(get_db)):
    request = shema.FilteredReview(reviewed_book_name=book_name,
                                   reviewed_author_name=author_name)

    return await fetch_filtered_review(request=request, response=response, db=db)
