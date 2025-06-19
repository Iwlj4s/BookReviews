from fastapi import HTTPException
from sqlalchemy import select, update, delete, and_, func

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.src.database import shema, models
from backend.src.database.models import Author


class AuthorDAO:
    @classmethod
    async def get_author_by_id(cls, db: AsyncSession, author_id: int):
        query = select(Author).where(Author.id == author_id)
        author = await db.execute(query)

        return author.scalars().first()


    @classmethod
    async def get_author_by_name(cls, db: AsyncSession, author_name: str):
        query = select(Author).where(Author.name == author_name.title())
        author = await db.execute(query)

        return author.scalars().first()

    @classmethod
    async def get_author_by_name_for_review(cls, request: shema.Review, db: AsyncSession):
        query = select(Author).where(Author.id == request.reviewed_book_author_id)
        authors = await db.execute(query)

        if not authors:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Автор не найден")

        return authors.scalars().all()

    @classmethod
    async def add_author(cls, request: shema.Author, db: AsyncSession):
        new_author = models.Author(
            name=request.name.title()
        )

        db.add(new_author)
        await db.commit()

        return new_author

    @classmethod
    async def change_author(cls, db: AsyncSession, author_id: int, data: dict):
        query = update(Author).where(Author.id == int(author_id)).values(
            name=data["name"]
        )

        await db.execute(query)
        await db.commit()

    @classmethod
    async def get_author_with_book_author_name(cls, db: AsyncSession, book):
        query = select(Author).where(Author.id == book.author_id)
        author = await db.execute(query)
        return author.scalars().first()

    @classmethod
    async def author_by_name(cls, db: AsyncSession, author_name: str):
        query = select(Author).where(Author.name == str(author_name.title()))
        author = await db.execute(query)
        return author.scalars().first()