import jwt
from jose import jwt, JWTError

from datetime import datetime, timezone

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from backend.config import get_auth_data
from backend.src.database import models, shema
from backend.src.database.database import get_db

from backend.src.helpers import password_helper
from backend.src.helpers.jwt_helper import create_access_token
from backend.src.helpers.token_helper import get_token


def sign_up(request: shema.User, response, db):
    email = db.query(models.User).filter(models.User.email == request.email).first()
    name = db.query(models.User).filter(models.User.name == request.name).first()

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
    db.commit()
    db.refresh(new_user)

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


def login(request: shema.User, response, db):
    user: models.User = db.query(models.User).filter(models.User.email == request.email).first()
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


def get_user(user_id, response, db):
    user: models.User = db.query(models.User).filter(models.User.id == user_id).first()

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


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(get_token)):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], auth_data['algorithm'])

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID пользователя')

    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    return user
