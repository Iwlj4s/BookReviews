from fastapi import Depends, APIRouter, Response

from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database.database import get_db
from backend.src.database.shema import User
from backend.src.database import shema, models
from backend.src.helpers.general_helper import CheckHTTP404NotFound

from backend.src.repository.user_repository import get_current_user, delete_current_user, change_current_user
from backend.src.repository import user_repository

from backend.src.DAO.general_dao import GeneralDAO

users_router = APIRouter(
    prefix="/book_reviews/users",
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
    response.delete_cookie(key='user_access_token')
    return {'message': 'Пользователь успешно вышел из системы'}


@users_router.get("/me/", status_code=200, tags=["users"])
async def get_me(response: Response,
                 user_data: User = Depends(get_current_user)):
    return user_data


@users_router.put("/change_me/", tags=["users"])
async def change_me(response: Response,
                    request: shema.User,
                    db: AsyncSession = Depends(get_db),
                    user_data: User = Depends(get_current_user)):

    return await user_repository.change_current_user(request, db, response, user_data)


@users_router.delete("/delete_me/", status_code=200, tags=["users"])
async def delete_me(response: Response,
                    user_data: User = Depends(get_current_user),
                    db: AsyncSession = Depends(get_db)):
    return await delete_current_user(user=user_data, db=db)


@users_router.get("/my_reviews/", tags=["users"])
async def get_my_reviews(user_data: shema.User = Depends(get_current_user)):
    return user_data.reviews


@users_router.post("/user/{user_id}", status_code=200, tags=["users"])
async def get_user(user_id: int,
                   db: AsyncSession = Depends(get_db)):
    user = await GeneralDAO.get_item_by_id(db=db, item=models.User, item_id=int(user_id))
    CheckHTTP404NotFound(founding_item=user, text="Пользователь не найден")
    return {
        'user_id:': user.id,
        'user_name:': user.name,
        'user_email': user.email,
        'reviews': user.reviews
    }


@users_router.post("/users_list")
async def get_users_for_user(db: AsyncSession = Depends(get_db)):
    users = await GeneralDAO.get_all_items(db=db, item=models.User)
    CheckHTTP404NotFound(founding_item=users, text="Пользователи не найдены")
    for user in users:
        return {
            'user_id:': user.id,
            'user_name:': user.name,
            'user_email': user.email,
            'reviews': user.reviews
        }

