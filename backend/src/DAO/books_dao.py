from fastapi import HTTPException
from sqlalchemy import select, update, delete, and_, func

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.src.database import shema, models
from backend.src.database.models import Book


class BookDAO:
    @classmethod
    async def get_book_by_id(cls, db: AsyncSession, book_id: int):
        query = select(Book).where(Book.id == book_id)
        book = await db.execute(query)

        return book.scalars().first()

    @classmethod
    async def get_book_by_book_name_for_review(cls, request: shema.Review, db: AsyncSession):
        query = select(Book).where(Book.id == request.reviewed_book_id)
        books = await db.execute(query)

        if not books:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")

        return books.scalars().all()

    @classmethod
    async def get_book_by_book_name(cls, book_name: str, author_id: int, db: AsyncSession):
        query = select(Book).where(
            (Book.author_id == author_id) & (Book.book_name == book_name.capitalize())
        )
        book = await db.execute(query)

        return book.scalars().first()

    @classmethod
    async def add_book(cls, request: shema.Book, book_cover, book_desc, author, db: AsyncSession):
        new_book = models.Book(
            book_cover=book_cover,
            book_name=request.book_name,
            author_id=author.id,
            book_description=book_desc
        )

        db.add(new_book)
        await db.commit()

        return new_book

    @classmethod
    async def change_book(cls, book_id: int, new_data, db: AsyncSession):
        query = update(Book).where(Book.id == int(book_id)).values(
            book_name=new_data["book_name"],
            book_description=new_data["book_description"]
        )

        await db.execute(query)
        await db.commit()

    @classmethod
    async def get_book_with_rating(cls, db: AsyncSession, book_id: int):
        book = await cls.get_book_by_id(db=db, book_id=book_id)
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Книга не найдена")

        rating_distribution = await db.execute(
            select(models.Review.rating, func.count(models.Review.id))
            .where(models.Review.reviewed_book_id == book_id)
            .where(models.Review.rating.isnot(None))
            .group_by(models.Review.rating)
        )
        rating_distribution = {rating: count for rating, count in rating_distribution}

        return {
            'book': book,
            'rating_status': {
                'avg': book.book_average_rating,
                'distribution': rating_distribution
            }
        }