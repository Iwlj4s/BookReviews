from fastapi import Depends, APIRouter, Response

from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.DAO.books_dao import BookDAO
from backend.src.database import shema, models
from backend.src.database.database import get_db

from backend.src.helpers.general_helper import CheckHTTP404NotFound

from backend.src.DAO.general_dao import GeneralDAO

books_router = APIRouter(
    prefix="/book_reviews/api/books",
    tags=["books"]
)


@books_router.get("/book/{book_id}", tags=["books"])
async def get_book(book_id,
                   db: AsyncSession = Depends(get_db)):
    book = await GeneralDAO.get_item_by_id(db=db, item=models.Book, item_id=int(book_id))
    CheckHTTP404NotFound(founding_item=book, text="Книга не найдены")
    return book


@books_router.get("/books_list", tags=["books"])
async def get_books(db: AsyncSession = Depends(get_db)):
    books = await GeneralDAO.get_all_items(db=db, item=models.Book)
    CheckHTTP404NotFound(founding_item=books, text="Книги не найдены")
    return books


@books_router.get("/book/{book_id}/stats", tags=["books"])
async def get_books_stats(book_id: int,
                          db:AsyncSession = Depends(get_db)):
    book_w_stats = await BookDAO.get_book_with_rating(db=db, book_id=book_id)
    return book_w_stats
