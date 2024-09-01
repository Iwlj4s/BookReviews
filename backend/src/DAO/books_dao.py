from sqlalchemy import select, update, delete, and_, func

from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database.models import Book


class BookDAO:
    @classmethod
    async def get_book_by_id(cls, db: AsyncSession, book_id: int):
        query = select(Book).where(Book.id == book_id)
        book = await db.execute(query)

        return book

    @classmethod
    async def get_book_by_name(cls, db: AsyncSession, book_name: str):
        query = select(Book).where(Book.id == book_name)
        book = await db.execute(query)

        return book

    @classmethod
    async def get_book_by_author(cls, db: AsyncSession, book_author: str):
        query = select(Book).where(Book.id == book_author)
        book = await db.execute(query)

        return book
