from fastapi import Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status

from backend.src.database import shema
from backend.src.DAO.reviews_dao import ReviewDAO
from backend.src.DAO.books_dao import BookDAO
from backend.src.DAO.authors_dao import AuthorDAO


def check_data_for_change_author(request: shema.Author, author, reviews):
    author_data = {}
    review_data = {}

    if request.name is None:
        author_data.update({"name": author})
    else:
        author_data.update({"name": request.name})

    for review in reviews:
        review_data.update({
            "reviewed_book_author_name": request.name if request.name else review.reviewed_book_author_name,
        })

    return author_data, review_data

