from typing import Optional

from sqlalchemy import select, update, delete, and_, func

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database import models
from src.database.models import Review, User

from celery_tasks.tasks import send_email_task


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
    async def get_reviews_desc(cls, db: AsyncSession):
        query = select(Review).order_by(models.Review.created.desc())

        result = await db.execute(query)

        return result.scalars().all()

    # --- DELETED REVIEWS --- #
    @classmethod
    async def send_deletion_email(cls,
                                  user: User,
                                  review: models.Review,
                                  book: models.Book,
                                  author: models.Author,
                                  reason: str):
        mail_theme = "Ваш обзор был удален"
        mail_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                    <h2 style="color: #d9534f;">Уведомление об удалении обзора</h2>
                    <p>Здравствуйте, {user.name}!</p>
                    <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #d9534f; margin: 15px 0;">
                        <p>Ваш обзор на книгу <strong>"{book.book_name}"</strong> автора <strong>{author.name}</strong> был удален.</p>
                        <p><strong>Причина:</strong> {reason}</p>
                    </div>
                    <h3>Содержание удаленного обзора:</h3>
                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px;">
                        <h4>{review.review_title}</h4>
                        <p>{review.review_body}</p>
                    </div>
                    <p style="margin-top: 20px;">Дата написания: {review.created.strftime('%d.%m.%Y')}</p>
                    <div style="margin-top: 30px; padding-top: 15px; border-top: 1px solid #eee;">
                        <p>Если это ошибка, свяжитесь с поддержкой.</p>
                        <p>С уважением,<br><strong>Команда BookReviews</strong></p>
                    </div>
                </div>
            </body>
        </html>
        """

        send_email_task.delay(mail_body, mail_theme, user.email)

    @classmethod
    async def create_deleted_review_record(cls,
                                           db: AsyncSession,
                                           review: Review,
                                           admin: User,
                                           reason: str):
        book = review.book
        author = review.author
        user = review.user

        deleted_review = models.DeletedReview(
            user_id=user.id,
            user_name=user.name,
            book_id=book.id,
            book_name=book.book_name,
            author_id=author.id,
            author_name=author.name,
            original_content=f"{review.review_title}\n{review.review_body}",
            rating=review.rating,
            reason=reason,
            admin_id=admin.id,
            review_id=review.id
        )
        db.add(deleted_review)
        await db.delete(review)
        await db.commit()
        await db.refresh(deleted_review)

        return deleted_review

    @classmethod
    async def load_review_with_relations(cls,
                                         db: AsyncSession,
                                         review_id: int) -> Optional[models.Review]:
        result = await db.execute(
            select(models.Review)
            .options(
                selectinload(models.Review.user),
                selectinload(models.Review.book),
                selectinload(models.Review.author)
            )
            .where(models.Review.id == review_id)
        )
        return result.scalar_one_or_none()

    @classmethod
    async def notify_user_about_deletion(cls,
                                         user_name: str,
                                         user_email: str,
                                         review_title: str,
                                         review_body: str,
                                         created_date: str,
                                         book_name:str,
                                         author_name: str,
                                         reason: str):
        mail_theme = "Ваш обзор был удален"
        mail_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                    <h2 style="color: #d9534f;">Уведомление об удалении обзора</h2>
                    <p>Здравствуйте, {user_name}!</p>
                    <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #d9534f; margin: 15px 0;">
                        <p>Ваш обзор на книгу <strong>"{book_name}"</strong> автора <strong>{author_name}</strong> был удален.</p>
                        <p><strong>Причина:</strong> {reason}</p>
                    </div>
                    <h3>Содержание удаленного обзора:</h3>
                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px;">
                        <h4>{review_title}</h4>
                        <p>{review_body}</p>
                    </div>
                    <p style="margin-top: 20px;">Дата написания: {created_date}</p>
                    <div style="margin-top: 30px; padding-top: 15px; border-top: 1px solid #eee;">
                        <p>Если это ошибка, свяжитесь с поддержкой.</p>
                        <p>С уважением,<br><strong>Команда BookReviews</strong></p>
                    </div>
                </div>
            </body>
        </html>
        """

        send_email_task.delay(mail_body, mail_theme, user_email)

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
            review_title=data["review_title"],
            review_body=data["review_body"],
            rating=data["rating"]
        )

        await db.execute(query)
        await db.commit()

        review = await db.get(Review, review_id)
        if review:
            await cls.update_book_rating(db, review.reviewed_book_id)

    @classmethod
    async def create_review(cls, request, user, book, author, db: AsyncSession):
        new_review = models.Review(
            created_by=user.id,
            reviewed_book_id=book.id,
            reviewed_book_cover=book.book_cover,
            reviewed_book_author_id=author.id,
            review_title=request.review_title,
            review_body=request.review_body,
            rating=request.rating,
            created=func.now(),
            updated=func.now()
        )

        db.add(new_review)
        await db.commit()
        await db.refresh(new_review)

        await cls.update_book_rating(db, book.id)
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

    @classmethod
    async def update_book_rating(cls, db: AsyncSession, book_id: int):
        found_avg_rating = await db.execute(
            select(func.avg(Review.rating))
            .where(Review.reviewed_book_id == book_id)
            .where(Review.rating.isnot(None))
        )
        avg_rating = round(found_avg_rating.scalar() or 0, 2)

        await db.execute(
            update(models.Book)
            .where(models.Book.id == book_id)
            .values(book_average_rating=avg_rating)
        )
        await db.commit()

    @classmethod
    async def is_review_deleted(cls, db: AsyncSession, review_id: int) -> bool:
        from backend.src.database import models
        from sqlalchemy import select
        existing = await db.execute(
            select(models.DeletedReview).where(models.DeletedReview.review_id == review_id)
        )
        return existing.scalars().first() is not None
