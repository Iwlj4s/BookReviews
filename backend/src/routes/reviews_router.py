from fastapi import Depends, APIRouter, Response

from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database.database import get_db
from backend.src.database.shema import User
from backend.src.database import shema


from backend.src.repository.user_repository import get_current_user
from backend.src.repository import reviews_repository
from backend.src.repository.reviews_repository import get_all_reviews, fetch_review, fetch_filtered_review

reviews_router = APIRouter(
    prefix="/book_reviews/reviews",
    tags=["reviews"]
)


@reviews_router.get("/", tags=["reviews"])
async def get_reviews(db: AsyncSession = Depends(get_db)):
    return await get_all_reviews(db=db)


@reviews_router.post("/create_review/", tags=["reviews"])
async def create_review(response: Response,
                        book_name: str,
                        book_author_name: str,
                        review_title: str,
                        review_body: str,
                        db: AsyncSession = Depends(get_db),
                        user: User = Depends(get_current_user)):

    request = shema.Review(reviewed_book_name=book_name,
                           reviewed_book_author_name=book_author_name,
                           review_title=review_title,
                           review_body=review_body)

    return await reviews_repository.create_review(request=request, response=response, user=user, db=db)


@reviews_router.put("/change_review/{review_id}", tags=["reviews"])
async def change_review(review_id: int,
                        new_review_title: str | None = None,
                        new_review_body: str | None = None,
                        db: AsyncSession = Depends(get_db),
                        user: User = Depends(get_current_user)):

    request = shema.ChangeReview(
        review_title=new_review_title,
        review_body=new_review_body)

    return await reviews_repository.change_review(review_id=int(review_id),
                                                  request=request,
                                                  db=db,
                                                  user=user)


@reviews_router.delete("/delete_review/{review_id}", tags=["reviews"])
async def delete_review(review_id: int,
                        db: AsyncSession = Depends(get_db),
                        user: User = Depends(get_current_user)):

    return await reviews_repository.delete_review(review_id=review_id, db=db, user=user)


@reviews_router.get("/{review_id}", tags=["reviews"])
async def get_review(review_id: int, response: Response, db: AsyncSession = Depends(get_db)):
    return await fetch_review(review_id=review_id, response=response, db=db)


@reviews_router.get("/filtered/", tags=["reviews"])
async def get_filtered_review(response: Response,
                              book_name: str | None = None,
                              author_name: str | None = None,
                              db: AsyncSession = Depends(get_db)):
    request = shema.FilteredReview(reviewed_book_name=book_name,
                                   reviewed_author_name=author_name)

    return await fetch_filtered_review(request=request, response=response, db=db)
