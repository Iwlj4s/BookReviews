from fastapi import Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from backend.src.DAO.users_dao import UserDAO


async def verify_user(db: AsyncSession, user_id: int):
    user = await UserDAO.get_user_by_id(db=db, user_id=int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    return user
