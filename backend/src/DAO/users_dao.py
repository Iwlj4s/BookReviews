from sqlalchemy import select, update, delete, and_, func

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.src.database.models import User


class UserDAO:
    @classmethod
    async def get_all_users(cls, db: AsyncSession):
        query = select(User)
        users = await db.execute(query)

        return users.scalars().all()

    @classmethod
    async def get_user_by_id(cls, db: AsyncSession, user_id: int):
        query = select(User).options(selectinload(User.reviews)).where(User.id == int(user_id))
        user = await db.execute(query)
        return user.scalars().first()

    @classmethod
    async def get_user_email(cls, db: AsyncSession, user_email: str):
        query = select(User).where(User.email == str(user_email))
        email = await db.execute(query)

        return email.scalars().first()

    @classmethod
    async def get_user_name(cls, db: AsyncSession, user_name: str):
        query = select(User).where(User.name == str(user_name))
        name = await db.execute(query)

        return name.scalars().first()

    @classmethod
    async def change_user(cls, db: AsyncSession, user_id: int, data: dict):
        query = update(User).where(User.id == int(user_id)).values(
            name=data["name"],
            email=data["email"],
            password=data["password"]
        )

        await db.execute(query)
        await db.commit()
