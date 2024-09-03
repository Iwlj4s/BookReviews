from fastapi import HTTPException
from sqlalchemy import select, update, delete, and_, func

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.src.database import shema
from backend.src.database.models import Book


class BookDAO:
    @classmethod
    async def get_book_by_id(cls, db: AsyncSession, book_id: int):
        query = select(Book).where(Book.id == book_id)
        book = await db.execute(query)

        return book

    @classmethod
    async def get_book_by_book_name_for_review(cls, request: shema.Review, db: AsyncSession):
        book = await db.scalar(
            select(Book).where(Book.book_name == request.reviewed_book_name)
        )

        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")

        return book

    @classmethod
    async def get_book_by_author(cls, db: AsyncSession, book_author: str):
        query = select(Book).where(Book.id == book_author)
        book = await db.execute(query)

        return book
