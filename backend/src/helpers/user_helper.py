from starlette.responses import Response

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.src.DAO.users_dao import UserDAO
from backend.src.database import shema
from backend.src.helpers import password_helper
from backend.src.helpers.jwt_helper import create_access_token


async def take_access_token_for_user(db: AsyncSession, response: Response, request: shema.UserSignIn, admin_check: bool):
    user = await UserDAO.get_user_email(db=db, user_email=str(request.email))
    if not user:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {
            'message': "Invalid email and/or password",
            'status_code': 403,
            'error': "FORBIDDEN"
        }

    if admin_check:
        if not user.is_admin:
            return {
                'message': "Недостаточно прав, вы не являетесь администратором",
                'status_code': 403,
                'error': "FORBIDDEN"
            }
        message = "Вы успешно зашли как администратор!"

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
        'user_access_token': access_token,
        'email': user.email,
        'name': user.name,
        'id': user.id
    }


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