from fastapi import Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status
from starlette.responses import Response

from backend.src.DAO.authors_dao import AuthorDAO
from backend.src.DAO.books_dao import BookDAO
from backend.src.DAO.users_dao import UserDAO
from backend.src.database.database import get_db
from backend.src.database import models, shema
from backend.src.helpers.reviews_helper import check_data_for_add_review

from backend.src.helpers.token_helper import get_token, verify_token

from backend.src.DAO.reviews_dao import ReviewDAO


async def create_review(request: shema.Review,
                        response: Response,
                        token: str = Depends(get_token),
                        db: AsyncSession = Depends(get_db)):
    user_id = verify_token(token=token)

    user = await UserDAO.get_user_by_id(db=db, user_id=int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    book, author = await check_data_for_add_review(request=request, db=db)

    new_review = models.Review(
        created_by=user_id,
        reviewed_book_id=book.id,
        reviewed_book_name=book.book_name,
        reviewed_book_author_name=author.name,
        review_title=request.review_title,
        review_body=request.review_body
    )
    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)

    return new_review


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
