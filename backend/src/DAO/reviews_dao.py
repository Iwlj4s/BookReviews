from fastapi import HTTPException
from sqlalchemy import select, update, delete, and_, func

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from backend.src.DAO.authors_dao import AuthorDAO
from backend.src.DAO.books_dao import BookDAO
from backend.src.database import shema, models
from backend.src.database.models import Review


class ReviewDAO:
    @classmethod
    async def get_all_reviews(cls, db: AsyncSession):
        query = select(Review)
        reviews = await db.execute(query)

        return reviews.scalars().all()

    @classmethod
    async def get_review_by_id(cls, db: AsyncSession, review_id: int):
        query = select(Review).options(selectinload(Review.user)).where(Review.id == int(review_id))
        review = await db.execute(query)
        return review.scalars().first()

    @classmethod
    async def get_filtered_reviews(cls, db: AsyncSession,
                                   book_name: str | None = None,
                                   author_name: str | None = None):
        query = select(Review)

        if book_name:
            query = query.where(Review.reviewed_book_name.ilike(f"%{book_name}%"))
        if author_name:
            query = query.where(Review.reviewed_book_author_name.ilike(f"%{author_name}%"))

        reviews = await db.execute(query)
        return reviews.scalars().all()

    @classmethod
    async def delete_review(cls, db: AsyncSession, review_id: int):
        query = delete(Review).where(Review.id == int(review_id))
        await db.execute(query)
        await db.commit()

    @classmethod
    async def change_review(cls, db: AsyncSession, review_id: int, data: dict):
        query = update(Review).where(Review.id == review_id).values(
            created_by=data["created_by"],
            reviewed_book_id=data["reviewed_book_id"],
            reviewed_book_name=data["reviewed_book_name"],
            reviewed_book_author_name=data["reviewed_book_author_name"],
            review_title=data["review_title"],
            review_body=data["review_body"]
        )

        await db.execute(query)
        await db.commit()

    @classmethod
    async def get_book_and_author(cls, request: shema.Review, db: AsyncSession):
        book = await BookDAO.get_book_by_book_name_for_review(request=request, db=db)
        author = await AuthorDAO.get_author_by_name_for_review(request=request, db=db)

        if book.author_id != author.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Имя автора не соответствует книге")

        return book, author

    @classmethod
    async def create_review(cls, request: shema.Review, user, book, author, db: AsyncSession):
        new_review = models.Review(
            created_by=user.id,
            reviewed_book_id=book.id,
            reviewed_book_name=book.book_name,
            reviewed_book_author_name=author.name,
            review_title=request.review_title,
            review_body=request.review_body
        )

        print(new_review)

        db.add(new_review)
        await db.commit()

        return new_review
