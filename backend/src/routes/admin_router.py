from fastapi import Depends, APIRouter, Response

from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.DAO.general_dao import GeneralDAO

from backend.src.database.database import get_db

from backend.src.repository import admin_repository
from backend.src.repository.admin_repository import get_current_admin_user

from backend.src.database.shema import User

from backend.src.database import models, shema

from backend.src.helpers.general_helper import CheckHTTP404NotFound

admin_router = APIRouter(
    prefix="/book_reviews/admin",
    tags=["admin"]
)


@admin_router.post("/sign_in", tags=["admin"])
async def sign_in_admin(user_email: str,
                        user_password: str,
                        response: Response,
                        db: AsyncSession = Depends(get_db)):
    request = shema.User(email=user_email,
                         password=user_password)

    return await admin_repository.login_admin(request=request,
                                              response=response,
                                              db=db)


@admin_router.post("/logout", tags=["admin"])
async def logout_admin(response: Response):
    response.delete_cookie(key='user_access_token')
    return {'message': 'Администратор успешно вышел из системы'}


# Users #
@admin_router.get("/users/get_users", tags=["admin"])
async def get_users(admin: User = Depends(get_current_admin_user),
                    db: AsyncSession = Depends(get_db)):
    users = await GeneralDAO.get_all_items(db=db, item=models.User)
    CheckHTTP404NotFound(founding_item=users, text="Пользователи не найден")

    return users


@admin_router.get("/users/get_user/{user_id}")
async def get_user(user_id: int,
                   admin: User = Depends(get_current_admin_user),
                   db: AsyncSession = Depends(get_db)):
    user = await GeneralDAO.get_item_by_id(db=db, item=models.User, item_id=int(user_id))
    CheckHTTP404NotFound(founding_item=user, text="Пользователь не найден")

    return user


@admin_router.put("/users/change_user/{user_id}")
async def change_user(user_id: int,
                      new_user_name: str | None = None,
                      new_user_email: str | None = None,
                      new_user_password: str | None = None,
                      admin: User = Depends(get_current_admin_user),
                      db: AsyncSession = Depends(get_db)):
    request = shema.User(
        name=new_user_name,
        email=new_user_email,
        password=new_user_password
    )

    return await admin_repository.change_user(user_id=user_id,
                                              request=request,
                                              admin=admin,
                                              db=db)


@admin_router.delete("/users/delete_user/{user_id}")
async def delete_user(user_id: int,
                      admin: User = Depends(get_current_admin_user),
                      db: AsyncSession = Depends(get_db)):
    return await admin_repository.delete_user(db=db, user_id=int(user_id))


# Reviews #
@admin_router.delete("/review/delete_review/{review_id}")
async def delete_review(review_id: int,
                        admin: User = Depends(get_current_admin_user),
                        db: AsyncSession = Depends(get_db)):
    return await GeneralDAO.delete_item(db=db, item=models.Review, item_id=int(review_id))


@admin_router.put("/review/change_review/{review_id}")
async def admin_change_review(review_id: int,
                              new_review_title: str | None = None,
                              new_review_body: str | None = None,
                              admin: User = Depends(get_current_admin_user),
                              db: AsyncSession = Depends(get_db)):
    request = shema.ChangeReview(
        review_title=new_review_title,
        review_body=new_review_body)

    return await admin_repository.change_review(review_id=review_id, request=request,
                                                admin=admin, db=db)


# Authors #
@admin_router.post("/authors/add_author", tags=["admin"])
async def add_author(response: Response,
                     name: str,
                     admin: User = Depends(get_current_admin_user),
                     db: AsyncSession = Depends(get_db)):
    request = shema.Author(name=name)

    return await admin_repository.add_author(response=response,
                                             request=request,
                                             admin=admin,
                                             db=db)


@admin_router.put("/authors/change_author", tags=["admin"])
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


@admin_router.delete("/authors/delete_author/{author_id}", tags=["admin"])
async def delete_author(author_id: int,
                        admin: User = Depends(get_current_admin_user),
                        db: AsyncSession = Depends(get_db)):
    return await admin_repository.delete_author(db=db, author_id=author_id, admin=admin)


# Books #
@admin_router.post("/books/add_book/", tags=["admin"])
async def add_book(book_name: str,
                   book_author_name: str,
                   book_description: str,
                   admin: User = Depends(get_current_admin_user),
                   db: AsyncSession = Depends(get_db)):
    request = shema.Book(
        book_name=str(book_name),
        book_author_name=str(book_author_name),
        book_description=str(book_description))

    return await admin_repository.add_book(request=request,
                                           admin=admin,
                                           db=db)

@admin_router.delete("/books/delete_book/{book_id}")
async def delete_book(book_id: int,
                      admin: User = Depends(get_current_admin_user),
                      db: AsyncSession = Depends(get_db)):
    return await admin_repository.delete_book(db=db, book_id=int(book_id))


@admin_router.put("/book/change_book/{book_id}")
async def change_book(book_id: int,
                      new_book_name: str | None = None,
                      new_book_description: str | None = None,
                      admin: User = Depends(get_current_admin_user),
                      db: AsyncSession = Depends(get_db)):
    request = shema.Book(
        book_name=new_book_name,
        book_description=new_book_description
    )

    return await admin_repository.change_book(db=db, book_id=int(book_id), request=request, admin=admin)
