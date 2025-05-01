from fastapi import Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status

from backend.src.database import shema
from backend.src.DAO.reviews_dao import ReviewDAO
from backend.src.DAO.books_dao import BookDAO
from backend.src.DAO.authors_dao import AuthorDAO


async def check_data_for_add_review(request: shema.Review, db: AsyncSession):
    book = await BookDAO.get_book_by_id(db=db, book_id=request.reviewed_book_id)
    author = await AuthorDAO.get_author_by_id(db=db, author_id=request.reviewed_book_author_id)

    if book.author_id == author.id:
        return book, author
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Имя автора не соответствует книге")


def check_data_for_change_review(request: shema.ChangeReview, review):
    data = {
        "review_title": request.review_title if request.review_title is not None else review.review_title,
        "review_body": request.review_body if request.review_body is not None else review.review_body,
        "rating": request.rating if request.rating is not None else review.rating
    }
    return data
