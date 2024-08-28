from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status

from backend.src.database import models, shema
from backend.src.database.database import get_db

from backend.src.helpers import password_helper


def sign_up(request: shema.User, response, db):
    email = db.query(models.User).filter(models.User.email == request.email).first()
    name = db.query(models.User).filter(models.User.name == request.name).first()

    if email:
        response.status_code = status.HTTP_409_CONFLICT

        return {
            'message': "User already exist",
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
        'message': "success",
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

    return {
        'message': "Success",
        'status_code': 200,
        'data': {
            'email': user.email,
            'name': user.name,
            'id': user.id
        },
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
