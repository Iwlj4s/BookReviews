from fastapi import Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status
from starlette.responses import Response

from backend.src.database.database import get_db
from backend.src.database import models, shema
from backend.src.database.models import User

from backend.src.helpers import password_helper
from backend.src.helpers.general_helper import CheckHTTP404NotFound, CheckHTTP401Unauthorized
from backend.src.helpers.jwt_helper import create_access_token

from backend.src.DAO.users_dao import UserDAO
from backend.src.DAO.authors_dao import AuthorDAO
from backend.src.repository.user_repository import get_current_user


async def login_admin(request: shema.User, response, db: AsyncSession = Depends(get_db)):
    user = await UserDAO.get_user_email(db=db, user_email=str(request.email))
    # TODO: Refactor this !!!
    if not user:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {
            'message': "Invalid email and/or password",
            'status_code': 403,
            'error': "FORBIDDEN"
        }

    if not user.is_admin:
        return {
            'message': "Недостаточно прав, вы не являетесь администратором",
            'status_code': 403,
            'error': "FORBIDDEN"
        }

    if not password_helper.verify_password(request.password, user.password):
        response.status_code = status.HTTP_403_FORBIDDEN
        return {
            'message': "Invalid email and/or password",
            'status_code': 403,
            'error': "FORBIDDEN"
        }

    # Creating access token #
    access_token = create_access_token({"sub": str(user.id)})
    # Write access token in cookie #
    response.set_cookie(key="user_access_token", value=access_token, httponly=True)

    return {
        'message': "Вы успешно зашли как администратор!",
        'status_code': 200,
        'data': {
            'email': user.email,
            'name': user.name,
            'id': user.id
        },
        'access_token': access_token
    }


async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        return current_user

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав!')


async def add_author(response: Response,
                     request: shema.Author,
                     admin: User = Depends(get_current_admin_user),
                     db: AsyncSession = Depends(get_db)):

    new_author = await AuthorDAO.add_author(request=request, db=db)
    await db.refresh(new_author)
    return {
        'message': "Автор добавлен успешно",
        'status_code': 200,
        'data': {
            'id': new_author.id,
            'Имя': new_author.name
        }
    }

