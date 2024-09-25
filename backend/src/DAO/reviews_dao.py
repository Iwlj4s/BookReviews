from sqlalchemy import select, update, delete, and_, func

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.src.database import shema, models
from backend.src.database.models import Review


class ReviewDAO:
    @classmethod
    async def get_reviews_by_book_author_id(cls, db: AsyncSession, review_book_author_id: int):
        query = select(Review).options(selectinload(Review.user)).where(Review.reviewed_book_author_id ==
                                                                        int(review_book_author_id))
        review = await db.execute(query)
        return review.scalars().all()

    @classmethod
    async def get_review_by_book_id(cls, db: AsyncSession, book_id: int):
        query = select(Review).options(selectinload(Review.user)).where(Review.reviewed_book_id == int(book_id))
        review = await db.execute(query)

        return review.scalars().all()

    @classmethod
    async def get_filtered_reviews(cls, db: AsyncSession,
                                   book_name: str | None = None,
                                   author_name: str | None = None):
        query = select(Review).options(selectinload(Review.user))

        if book_name:
            query = query.where(Review.reviewed_book_name.ilike(f"%{book_name}%"))
        if author_name:
            query = query.where(Review.reviewed_book_author_name.ilike(f"%{author_name}%"))

        reviews = await db.execute(query)
        return reviews.scalars().all()

    @classmethod
    async def change_review(cls, db: AsyncSession, review_id: int, data: dict):
        query = update(Review).where(Review.id == review_id).values(
            created_by=data["created_by"],
            reviewed_book_id=data["reviewed_book_id"],
            reviewed_book_author_id=data["reviewed_book_author_id"],
            reviewed_book_name=data["reviewed_book_name"],
            reviewed_book_author_name=data["reviewed_book_author_name"],
            review_title=data["review_title"],
            review_body=data["review_body"]
        )

        await db.execute(query)
        await db.commit()

    @classmethod
    async def create_review(cls, request: shema.Review, user, book, author, db: AsyncSession):
        new_review = models.Review(
            created_by=user.id,
            reviewed_book_id=book.id,
            reviewed_book_cover=book.book_cover,
            reviewed_book_author_id=author.id,
            reviewed_book_name=book.book_name,
            reviewed_book_author_name=author.name,
            review_title=request.review_title,
            review_body=request.review_body
        )

        print(new_review)

        db.add(new_review)
        await db.commit()

        return new_review

    @classmethod
    async def change_reviewed_book_author_name(cls, db: AsyncSession, old_author_name: str, r_data: dict):
        review_query = update(Review).options(selectinload(Review.user)).where(Review.reviewed_book_author_name ==
                                                                               str(old_author_name)).values(
            reviewed_book_author_name=r_data["reviewed_book_author_name"]
        )

        await db.execute(review_query)
        await db.commit()

    @classmethod
    async def change_reviewed_book_name(cls, db: AsyncSession, old_book_name: str, r_data: dict):
        review_query = update(Review).options(selectinload(Review.user)).where(Review.reviewed_book_name ==
                                                                               str(old_book_name)).values(
            reviewed_book_name=r_data["book_name"]
        )

        await db.execute(review_query)
        await db.commit()

    @classmethod
    async def delete_review_by_user_id(cls, db: AsyncSession, user_id: int):
        query = delete(Review).options(selectinload(Review.user)).where(Review.created_by == int(user_id))
        await db.execute(query)
        await db.commit()
