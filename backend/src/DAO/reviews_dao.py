from sqlalchemy import select, update, delete, and_, func

from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database.models import Review


class ReviewDAO:
    @classmethod
    async def get_all_reviews(cls, db: AsyncSession):
        query = select(Review)
        reviews = await db.execute(query)

        return reviews.scalars().all()

    @classmethod
    async def get_review_by_id(cls, db: AsyncSession, review_id: int):
        query = select(Review).where(Review.id == int(review_id))

        review = await db.execute(query)

        return review.scalars().first()

    @classmethod
    async def get_filtered_reviews(cls, db: AsyncSession,
                                   book_name: str | None = None,
                                   author_name: str | None = None):
        query = select(Review)

        if book_name:
            query = query.where(Review.reviewed_book_name.ilike(f"%{book_name}%"))  # Нечувствительный поиск
        if author_name:
            query = query.where(Review.reviewed_book_author_name.ilike(f"%{author_name}%"))  # Нечувствительный поиск

        reviews = await db.execute(query)
        return reviews.scalars().all()

    @classmethod
    async def delete_review(cls, db: AsyncSession, review_id: int):
        query = delete(Review).where(Review.id == int(review_id))
        await db.execute(query)
        await db.commit()