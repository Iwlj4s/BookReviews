from sqlalchemy import select, update, delete, and_, func

from sqlalchemy.ext.asyncio import AsyncSession


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
