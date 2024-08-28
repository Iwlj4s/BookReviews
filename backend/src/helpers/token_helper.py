from fastapi import Request, HTTPException, status, Depends
from fastapi import Response


def get_token(request: Request, response: Response):
    token = request.cookies.get('user_access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')

    return token
