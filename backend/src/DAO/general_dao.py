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
        result = await db.execute(query)
        return result.scalars().first()
