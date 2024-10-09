from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status
from starlette.responses import Response

from backend.src.database.database import get_db
from backend.src.database import models, shema

from backend.src.helpers import password_helper, user_helper
from backend.src.helpers.general_helper import CheckHTTP404NotFound, CheckHTTP401Unauthorized
from backend.src.helpers.token_helper import get_token, verify_token

from backend.src.DAO.general_dao import GeneralDAO
from backend.src.DAO.users_dao import UserDAO
from backend.src.helpers.user_helper import check_data_for_change_user


async def sign_up(request: shema.User, response, db: AsyncSession):
    email = await UserDAO.get_user_email(db=db, user_email=str(request.email))
    name = await UserDAO.get_user_name(db=db, user_name=str(request.name))

    if email:
        response.status_code = status.HTTP_409_CONFLICT

        return {
            'message': "Email already exist",
            'status_code': 409,
            'error': "CONFLICT"
        }

    if name:
        response.status_code = status.HTTP_409_CONFLICT

        return {
            'message': "This username already exists",
            'status_code': 409,
            'error': "CONFLICT"
        }

    hash_password = password_helper.hash_password(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hash_password)
    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)

    return {
        'message': "Register successfully",
        'status_code': 201,
        'status': "success",
        'data': {
            'id': new_user.id,
            'user_name': new_user.name,
            'user_email': new_user.email
        }
    }


async def login(request: shema.UserSignIn,
                response: Response,
                db: AsyncSession):
    user = await user_helper.take_access_token_for_user(db=db,
                                                        response=response,
                                                        request=request,
                                                        admin_check=False)
    return {
        "user_access_token": user['user_access_token'],
        "email": user['email'],
        "name": user['name'],
        "id": user['id']
    }


async def get_current_user(db: AsyncSession = Depends(get_db),
                           token: str = Depends(get_token)):
    user_id = verify_token(token=token)

    user = await GeneralDAO.get_item_by_id(db=db, item=models.User, item_id=int(user_id))
    CheckHTTP401Unauthorized(founding_item=user, text="Пользователь не найден")

    return user


async def delete_current_user(user: shema.User,
                              db: AsyncSession = Depends(get_db)):
    await db.delete(user)
    await db.commit()

    return {
        'message': "success",
        'status_code': 200,
        'status': 'Success',
        'data': {f"User id:{user.id}",
                 f" name:{user.name}",
                 f" email:{user.email} deleted!"
        }
    }


async def change_current_user(request: shema.User,
                              db: AsyncSession,
                              response: Response,
                              user: shema.User):
    new_data = check_data_for_change_user(request=request, user=user)

    if new_data.get("password") != user.password:
        response.delete_cookie(key='user_access_token')

    await UserDAO.change_user(db=db,
                              user_id=user.id,
                              data=new_data)

    await db.refresh(user)

    return {
        'message': "User updated successfully",
        'status_code': 200,
        'data': {
            'id': user.id,
            'user_name': new_data.get("name"),
            'user_email': new_data.get("email")
        }
    }
