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
    async def get_book_by_name(cls, db: AsyncSession, book_name: str):
        query = select(Book).where(Book.book_name == book_name)
        book = await db.execute(query)
        return book.scalars().first()

    @classmethod
    async def get_book_by_book_name_for_review(cls, request: shema.Review, db: AsyncSession):
        query = select(Book).where(Book.book_name == request.reviewed_book_name)
        books = await db.execute(query)

        if not books:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")

        return books.scalars().all()

    @classmethod
    async def get_book_by_author(cls, db: AsyncSession, book_author: str):
        query = select(Book).where(Book.id == book_author)
        book = await db.execute(query)

        return book

    @classmethod
    async def get_book_with_author(cls, db: AsyncSession, author):
        query = select(Book).where(Book.author_id == author.id)
        book = await db.execute(query)

        return book.scalars().first()
