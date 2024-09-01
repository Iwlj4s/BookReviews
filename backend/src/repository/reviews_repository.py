from fastapi import Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status
from starlette.responses import Response

from backend.src.database.database import get_db
from backend.src.database import models, shema

from backend.src.helpers.token_helper import get_token, verify_token

from backend.src.DAO.reviews_dao import ReviewDAO
from backend.src.helpers.user_helper import verify_user


# TODO: Did fetch review_book_name and review_book_author_name id by review_book_id
# book_stuff = await ...(review_book_name, review_book_author_name)
# book_stuff.book_name, book_stuff.author_name


async def get_all_reviews(db: AsyncSession = Depends(get_db)):
    reviews = await ReviewDAO.get_all_reviews(db=db)

    if not reviews:
        return {
            'message': "Обзоры отсутствуют",
            'status_code': status.HTTP_404_NOT_FOUND,
            'error': "NOT FOUND"
        }

    return reviews


async def fetch_review(review_id: int, response: Response, db: AsyncSession = Depends(get_db)):
    review = await ReviewDAO.get_review_by_id(db=db, review_id=review_id)

    if not review:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            'message': "Not found",
            'status_code': 404,
            'error': 'NOT FOUND'}

    return review


async def fetch_filtered_review(request: shema.FilteredReview,
                                response: Response,
                                db: AsyncSession = Depends(get_db)):

    reviews = await ReviewDAO.get_filtered_reviews(db=db,
                                                   book_name=request.reviewed_book_name,
                                                   author_name=request.reviewed_author_name)

    if not reviews:
        return {
            'message': "Обзоры не найдены",
            'status_code': status.HTTP_404_NOT_FOUND,
            'error': "NOT FOUND"
        }

    return reviews
