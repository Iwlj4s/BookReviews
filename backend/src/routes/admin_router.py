from fastapi import Depends, APIRouter, Response

from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database.database import get_db
from backend.src.database.shema import User
from backend.src.database import shema
from backend.src.repository import admin_repository

admin_router = APIRouter(
    prefix="/book_reviews/admin",
    tags=["admins"]
)


@admin_router.post("/sign_in", tags=["admins"])
async def sign_in_admin(user_email: str,
                        user_password: str,
                        response: Response,
                        db: AsyncSession = Depends(get_db)):
    request = shema.User(email=user_email,
                         password=user_password)

    return await admin_repository.login_admin(request=request,
                                              response=response,
                                              db=db)


@admin_router.post("/logout", tags=["admins"])
async def logout_admin(response: Response):
    response.delete_cookie(key='user_access_token')
    return {'message': 'Администратор успешно вышел из системы'}
