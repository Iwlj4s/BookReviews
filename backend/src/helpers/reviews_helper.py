from fastapi import Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status

from backend.src.database import shema
from backend.src.DAO.reviews_dao import ReviewDAO
from backend.src.DAO.books_dao import BookDAO
from backend.src.DAO.authors_dao import AuthorDAO


async def check_data_for_add_review(request: shema.Review, db: AsyncSession):
    books = await BookDAO.get_book_by_book_name_for_review(request=request, db=db)
    authors = await AuthorDAO.get_author_by_name_for_review(request=request, db=db)

    for book in books:
        for author in authors:
            if book.author_id == author.id:
                return book, author

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Имя автора не соответствует книге")


def check_data_for_change_review(request: shema.ChangeReview, review):
    data = {}
    data.update({"created_by": review.created_by})
    data.update({"reviewed_book_id": review.reviewed_book_id})
    data.update({"reviewed_book_author_id": review.reviewed_book_author_id})
    data.update({"reviewed_book_name": review.reviewed_book_name})
    data.update({"reviewed_book_author_name": review.reviewed_book_author_name})

    if request.review_title is None:
        data.update({"review_title": review.review_title})
    else:
        data.update({"review_title": request.review_title})

    if request.review_body is None:
        data.update({"review_body": review.review_body})
    else:
        data.update({"review_body": request.review_body})

    return data