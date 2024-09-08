from fastapi import Depends, APIRouter, Response

from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.DAO.authors_dao import AuthorDAO
from backend.src.database.database import get_db
from backend.src.database.models import Author
from backend.src.database.shema import User
from backend.src.database import shema
from backend.src.repository import admin_repository
from backend.src.repository.admin_repository import get_current_admin_user

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


# Authors #
@admin_router.post("/authors/add_author", tags=["admins"])
async def add_author(response: Response,
                     name: str,
                     admin: User = Depends(get_current_admin_user),
                     db: AsyncSession = Depends(get_db)):
    request = shema.Author(name=name)

    return await admin_repository.add_author(response=response,
                                             request=request,
                                             admin=admin,
                                             db=db)


@admin_router.get("/authors/get_authors", tags=["admins"])
async def get_authors(admin: User = Depends(get_current_admin_user),
                      db: AsyncSession = Depends(get_db)):
    return await AuthorDAO.get_all_authors(db=db)


@admin_router.put("/authors/change_author", tags=["admins"])
async def change_author(response: Response,
                        author_id: int,
                        new_name: str | None = None,
                        admin: User = Depends(get_current_admin_user),
                        db: AsyncSession = Depends(get_db)):
    request = shema.Author(name=new_name)

    return await admin_repository.change_author(response=response,
                                                author_id=author_id,
                                                request=request,
                                                admin=admin,
                                                db=db)


@admin_router.delete("/authors/delete_author/{author_id}")
async def delete_author(author_id: int,
                        admin: User = Depends(get_current_admin_user),
                        db: AsyncSession = Depends(get_db)):

    return await admin_repository.delete_author(db=db, author_id=author_id, admin=admin)


@admin_router.get("/authors/get_author/{author_id}", tags=["admins"])
async def get_author(author_id: int,
                     admin: User = Depends(get_current_admin_user),
                     db: AsyncSession = Depends(get_db)):

    return await AuthorDAO.get_author_by_id(db=db, author_id=author_id)

