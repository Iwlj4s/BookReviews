from fastapi import Request, HTTPException, status, Depends
from fastapi import Response

from jose import jwt, JWTError
from datetime import datetime, timezone
from backend.config import get_auth_data


def get_token(request: Request, response: Response):
    token = request.cookies.get('user_access_token')  # Если вы используете куки
    if not token:
        token = request.headers.get('Authorization')  # Попробуйте получить токен из заголовков
        if token:
            token = token.split(" ")[1]  # Извлеките токен из заголовка Authorization
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')

    return token


def verify_token(token: str):
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

    return user_id
