from sqlalchemy import select, update, delete, and_, func

from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database.models import Author


class AuthorDAO:
    @classmethod
    async def get_author_by_name(cls, db: AsyncSession, author_name: str):
        query = select(Author).where(Author.name == author_name)
        author = await db.execute(query)
        return author.scalars().first()
