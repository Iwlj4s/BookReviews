from typing import List

from fastapi import Depends, APIRouter, Response

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_db
from src.database.shema import User, UserOut, ReviewOut
from src.database import shema, models
from src.helpers.general_helper import CheckHTTP404NotFound

from src.repository.user_repository import get_current_user, delete_current_user, change_current_user
from src.repository import user_repository

from src.DAO.general_dao import GeneralDAO

users_router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)


@users_router.post("/sign_up", status_code=201, tags=["users"])
async def sign_up(request: shema.UserSignUp,
                  response: Response,
                  db: AsyncSession = Depends(get_db)):
    return await user_repository.sign_up(request, response, db)


@users_router.post("/sign_in", status_code=200, tags=["users"])
async def sign_in(request: shema.UserSignIn,
                  response: Response,
                  db: AsyncSession = Depends(get_db)):
    return await user_repository.login(request, response, db)


@users_router.post("/logout", tags=["users"])
async def logout(response: Response):
    response.delete_cookie(key='user_access_token', secure=True, domain='127.0.0.1', path='/')
    response.delete_cookie(key='user_access_token', secure=True, domain='localhost', path='/')
    return {'message': 'Пользователь успешно вышел из системы'}


async def review_to_out(review):
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
    print(data)
    return {
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


@users_router.get("/me/", status_code=200, tags=["users"], response_model=UserOut)
async def get_me(response: Response, user_data: User = Depends(get_current_user)):
    reviews = [await review_to_out(r) for r in user_data.reviews]
    return {
        "id": user_data.id,
        "name": user_data.name,
        "email": user_data.email,
        "is_admin": user_data.is_admin,
        "bio": user_data.bio,
        "reviews": reviews
    }


@users_router.put("/change_me/", tags=["users"])
async def change_me(response: Response,
                    request: shema.ChangeUser,
                    db: AsyncSession = Depends(get_db),
                    user_data: shema.ChangeUser = Depends(get_current_user)):
    return await user_repository.change_current_user(request, db, response, user_data)


@users_router.delete("/delete_me/", status_code=200, tags=["users"])
async def delete_me(response: Response,
                    user_data: User = Depends(get_current_user),
                    db: AsyncSession = Depends(get_db)):
    return await delete_current_user(user=user_data, db=db)


@users_router.get("/my_reviews/", tags=["users"], response_model=List[ReviewOut])
async def get_my_reviews(user_data: User = Depends(get_current_user)):
    return [await review_to_out(r) for r in user_data.reviews]


@users_router.post("/user/{user_id}", status_code=200, tags=["users"], response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await GeneralDAO.get_item_by_id(db=db, item=models.User, item_id=int(user_id))
    CheckHTTP404NotFound(founding_item=user, text="Пользователь не найден")
    reviews = [await review_to_out(r) for r in user.reviews]
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "is_admin": user.is_admin,
        "bio": user.bio,
        "reviews": reviews
    }


@users_router.get("/user/{user_id}", status_code=200, tags=["users"], response_model=UserOut)
async def get_other_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await GeneralDAO.get_item_by_id(db=db, item=models.User, item_id=int(user_id))
    CheckHTTP404NotFound(founding_item=user, text="Пользователь не найден")
    reviews = [await review_to_out(r) for r in user.reviews]
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "is_admin": user.is_admin,
        "bio": user.bio,
        "reviews": reviews
    }


@users_router.get("/users_list", status_code=200, tags=["users"], response_model=List[shema.SimpleUser])
async def get_users_for_user(db: AsyncSession = Depends(get_db)):
    users = await GeneralDAO.get_all_items(db=db, item=models.User)
    CheckHTTP404NotFound(founding_item=users, text="Пользователи не найдены")
    users_list = []
    for user in users:
        reviews = [await review_to_out(r) for r in user.reviews]
        users_list.append({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'bio': user.bio,
            'profile_picture': user.profile_picture,
            'registration_date': user.registration_date,
            'warnings': user.warnings,
            'is_active': user.is_active,
            'is_user': user.is_user,
            'is_admin': user.is_admin,
            'reviews': reviews
        })
    return users_list
