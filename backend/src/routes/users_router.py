from fastapi import Depends, APIRouter, Response

from sqlalchemy.ext.asyncio import AsyncSession

from typing import Optional

from backend.src.database.database import get_db
from backend.src.database.shema import User
from backend.src.database import shema
from backend.src.helpers.token_helper import get_token

from backend.src.repository.user_repository import get_current_user, delete_current_user, change_current_user
from backend.src.repository import user_repository

users_router = APIRouter(
    prefix="/book_reviews/users",
    tags=["users"]
)


# TODO: Create /reviews for check all reviews by user
# TODO: Add (All by user): add review, delete review, change review
@users_router.post("/sign_up", status_code=201, tags=["users"])
async def sign_up(user_name: str,
                  user_email: str,
                  user_password: str,
                  response: Response,
                  db: AsyncSession = Depends(get_db)):
    request = shema.User(name=user_name,
                         email=user_email,
                         password=user_password)
    return await user_repository.sign_up(request, response, db)


@users_router.post("/sign_in", status_code=200, tags=["users"])
async def sign_in(user_email: str,
                  user_password: str,
                  response: Response,
                  db: AsyncSession = Depends(get_db)):
    request = shema.User(email=user_email,
                         password=user_password)
    return await user_repository.login(request, response, db)


@users_router.get("/{user_id}", status_code=200)
async def get_user(user_id: int,
                   response: Response,
                   db: AsyncSession = Depends(get_db)):
    return await user_repository.get_user(user_id, response, db)


@users_router.get("/me/", status_code=200)
async def get_me(response: Response,
                 user_data: User = Depends(get_current_user)):
    return user_data


@users_router.delete("/delete_me/", status_code=200)
async def delete_me(response: Response,
                    user_data: User = Depends(delete_current_user)):
    return user_data


@users_router.put("/change_me/")
async def change_me(response: Response,
                    new_user_name: str | None = None,
                    new_user_email: str | None = None,
                    new_user_password: str | None = None,
                    db: AsyncSession = Depends(get_db),
                    token: str = Depends(get_token)):
    request = shema.User(name=new_user_name,
                         email=new_user_email,
                         password=new_user_password)

    return await user_repository.change_current_user(request, db, response, token)


@users_router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key='user_access_token')
    return {'message': 'Пользователь успешно вышел из системы'}
