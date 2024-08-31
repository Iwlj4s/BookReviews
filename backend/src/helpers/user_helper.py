from fastapi import Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from backend.src.DAO.users_dao import UserDAO
from backend.src.database import shema
from backend.src.helpers import password_helper


async def verify_user(db: AsyncSession, user_id: int):
    user = await UserDAO.get_user_by_id(db=db, user_id=int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    return user


def check_data_for_change_user(request: shema.User, user):
    data = {}

    if request.name is None:
        data.update({"name": user.name})
    else:
        data.update({"name": request.name})

    if request.email is None:
        data.update({"email": user.email})
    else:
        data.update({"email": request.email})

    if request.password is None:
        data.update({"password": user.password})
    else:
        hash_password = password_helper.hash_password(request.password)
        data.update({"password": hash_password})

    return data
