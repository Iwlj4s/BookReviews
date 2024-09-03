from fastapi import HTTPException
from sqlalchemy import select, update, delete, and_, func

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.src.database import shema
from backend.src.database.models import Author


class AuthorDAO:
    @classmethod
    async def get_author_by_name(cls, db: AsyncSession, author_name: str):
        query = select(Author).where(Author.name == author_name)
        author = await db.execute(query)
        return author.scalars().first()

    @classmethod
    async def get_author_by_name_for_review(cls, request: shema.Review, db: AsyncSession):
        author = await db.scalar(
            select(Author)
            .filter(Author.name == request.reviewed_book_author_name)
        )

        if not author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Автор не найден")

        return author
