from sqlalchemy import select, update, delete, and_, func

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from backend.celery.tasks import send_email_task
from backend.src.database import models
from backend.src.database.models import User


class UserDAO:
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
            bio=data["bio"],
            password=data["password"]
        )

        await db.execute(query)
        await db.commit()

    @classmethod
    async def get_user_by_id(cls, db: AsyncSession, user_id: int):
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)

        return result.scalar_one_or_none() 

    @classmethod
    async def get_all_users(cls, db: AsyncSession):
        query = select(User)
        users = await db.execute(query)

        return users.scalars().all()

    @classmethod
    async def get_simple_user(cls, db: AsyncSession, user_id: int):
        query = select(User).where(User.id == user_id).options(load_only(
            User.id,
            User.name,
            User.email,
            User.is_active,
            User.is_admin
        ))
    
    @classmethod
    async def get_user_by_email(cls, email: str, db: AsyncSession):
        print(f"Executing query for email: {email}")
        query = select(User).where(User.email == str(email))
        result = await db.execute(query)

        user = result.scalars().first()

        if user is None:
            print(f"No user found with email: {email}")

        return user


    @classmethod
    async def add_admin(cls, user_id: int, db: AsyncSession):
        # Просто выполняем UPDATE запрос
        await db.execute(
            update(User)
            .where(User.id == user_id)
            .values(is_admin=True)
        )
        await db.commit()

    @classmethod
    async def notify_user_about_new_rights(cls,
                                         user_name: str,
                                         user_email: str):
        mail_theme = "Ваш новый статус администратора BookReviews"
        mail_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                    <h2 style="color: #2c3e50; border-bottom: 2px solid #dce055; padding-bottom: 10px;">
                        {mail_theme}
                    </h2>
                    
                    <p>Здравствуйте, {user_name}!</p>
                    
                    <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #dce055; margin: 15px 0;">
                        <p style="margin: 0;"><strong>Мы рады сообщить, что Вам присвоены права администратора платформы BookReviews!</strong></p>
                    </div>
                    
                    <p>Теперь в Ваши обязанности входит:</p>
                    <ul style="padding-left: 20px; color: #2c3e50;">
                        <li>Модерация контента</li>
                        <li>Управление пользователями</li>
                        <li>Добавление новых книг и авторов</li>
                        <li>Решение спорных ситуаций</li>
                    </ul>
                    
                    <p style="background-color: #f0f4f8; padding: 10px; border-radius: 4px;">
                        🔐 <strong>Панель администратора находится в Вашем профиле</strong> 
                    </p>
                    
                    <div style="margin-top: 30px; padding-top: 15px; border-top: 1px solid #eee; color: #7f8c8d;">
                        <p>Если у Вас есть вопросы, пожалуйста, ответьте на это письмо.</p>
                        <p>С уважением,<br>
                        <strong style="color: #2c3e50;">Команда BookReviews</strong></p>
                    </div>
                </div>
            </body>
        </html>
        """

        send_email_task.delay(mail_body, mail_theme, user_email)