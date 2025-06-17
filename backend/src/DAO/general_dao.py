from sqlalchemy import select, update, delete, and_, func, desc
from sqlalchemy.orm import selectinload

from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database import models


class GeneralDAO:
    @classmethod
    async def get_all_items(cls, db: AsyncSession, item):
        """
        :param db: database
        :param item: Founding item, like models.User
        :return: Founded items
        """
        query = select(item)
        items = await db.execute(query)

        return items.scalars().all()

    @classmethod
    async def get_item_by_id(cls, db: AsyncSession, item, item_id: int):
        """
        :param db: database
        :param item: Founding item, like models.User
        :param item_id: Item id
        :return: Founded item
        """

        query = select(item).where(item.id == item_id)
        item = await db.execute(query)

        return item.scalars().first()

    @classmethod
    async def delete_item(cls, db: AsyncSession, item, item_id: int):
        """
        :param db: database
        :param item: deleting item
        :param item_id: item id
        :return: nothing
        """

        query = delete(item).where(item.id == int(item_id))

        await db.execute(query)
        await db.commit()

    @classmethod
    async def get_last_record(cls, db: AsyncSession, item):
        """
        :param db: database
        :param item: founding item
        :return:
        """
        query = select(item).order_by(desc(item.id))
        last_record = await db.execute(query)
        return last_record.scalars().first()

    @classmethod
    async def get_last_review_with_relations(cls, db: AsyncSession):
        query = (
        select(models.Review)
        .options(
            selectinload(models.Review.book),  # assuming relation Review.book
            selectinload(models.Review.author),  # assuming relation Review.author
            selectinload(models.Review.user)  # assuming relation Review.user
        )
        .order_by(desc(models.Review.id))
    )
    
        # Получаем результат запроса
        result = await db.execute(query)
        
        # Извлекаем первый объект Review
        review = result.scalars().first()

        # Проверяем, что review не None
        if review is None:
            print("No reviews found.")
            return None

        # Формируем данные для возврата
        data = {
            "id": review.id,
            "review_title": review.review_title,
            "review_body": review.review_body,
            "rating": review.rating,
            "reviewed_book_id": review.reviewed_book_id,
            "reviewed_book_name": review.book.book_name if getattr(review, 'book', None) else None,
            "reviewed_book_author_id": review.reviewed_book_author_id,
            "reviewed_book_author_name": review.author.name if getattr(review, 'author', None) else None,
            "reviewed_book_cover": review.book.book_cover if getattr(review, 'book', None) else review.reviewed_book_cover,
            "reviewed_book_description": review.book.book_description,
            "updated": review.updated,
            "created": review.created,
            "user_id": review.user.id if getattr(review, 'user', None) else None,
            "user_name": review.user.name if getattr(review, 'user', None) else None,
        }

        print(f"REVIEW DATA: \n {data} ")

        return data  # Возвращаем сформированные данные
