from fastapi import Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status
from starlette.responses import Response

from backend.src.database.database import get_db
from backend.src.database import models, shema

from backend.src.helpers import password_helper
from backend.src.helpers.jwt_helper import create_access_token
from backend.src.helpers.token_helper import get_token, verify_token

from backend.src.DAO.users_dao import UserDAO
from backend.src.helpers.user_helper import verify_user, check_data_for_change_user


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
            'email': new_user.email
        }
    }


async def login(request: shema.User, response, db: AsyncSession):
    user = await UserDAO.get_user_email(db=db, user_email=str(request.email))
    if not user:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {
            'message': "Invalid email and/or password",
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
        'message': "Success",
        'status_code': 200,
        'data': {
            'email': user.email,
            'name': user.name,
            'id': user.id
        },
        'access_token': access_token
    }


async def fetch_user(user_id, response, db: AsyncSession = Depends(get_db)):
    user = await UserDAO.get_user_by_id(db=db, user_id=int(user_id))
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            'message': "Not found",
            'status_code': 404,
            'error': 'NOT FOUND'
        }
    return {
        'message': "success",
        'status_code': 200,
        'status': 'Success',
        'data': user
    }


async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(get_token)):
    user_id = verify_token(token=token)

    user = await UserDAO.get_user_by_id(db=db, user_id=int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    return {
        'message': "success",
        'status_code': 200,
        'status': 'Success',
        'data': user
    }


async def delete_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(get_token)):
    user_id = verify_token(token=token)

    user = await UserDAO.get_user_by_id(db=db, user_id=int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    await db.delete(user)
    await db.commit()

    return {
        'message': "success",
        'status_code': 200,
        'status': 'Success',
        'data': f"User id:{user.id} name:{user.name} email:{user.email} deleted!"
    }


async def change_current_user(request: shema.User, db: AsyncSession, response: Response, token: str):
    user_id = verify_token(token=token)

    user = await verify_user(db, user_id=user_id)

    new_data = check_data_for_change_user(request=request, user=user)

    if new_data.get("password") != user.password:
        response.delete_cookie(key='user_access_token')

    await UserDAO.change_user(db=db,
                              user_id=user_id,
                              data=new_data)

    return {
        'message': "User updated successfully",
        'status_code': 200,
        'data': {
            'id': user_id,
            'name': new_data.get("name"),
            'email': new_data.get("email")
        }
    }
