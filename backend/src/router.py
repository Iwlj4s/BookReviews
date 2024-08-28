from fastapi import Depends, APIRouter, Response
from sqlalchemy.orm import Session
from backend.src.database import shema
from backend.src.database.database import get_db

from backend.src.repository import user_repository


router = APIRouter(
    prefix="/book_reviews/users",
    tags=["users"]
)


# TODO: Create change user function and delete user function
@router.post("/sign_up", status_code=201, tags=["users"])
async def sign_up(user_name: str,
                  user_email: str,
                  user_password: str,
                  response: Response,
                  db: Session = Depends(get_db)):
    request = shema.User(name=user_name,
                         email=user_email,
                         password=user_password)
    return user_repository.sign_up(request, response, db)


@router.post("/sign_in", status_code=200, tags=["users"])
async def sign_in(user_email: str,
                  user_password: str,
                  response: Response,
                  db: Session = Depends(get_db)):
    request = shema.User(email=user_email,
                         password=user_password)
    return user_repository.login(request, response, db)


@router.get("/{user_id}", status_code=200)
async def get_user(user_id: int,
                   response: Response,
                   db: Session = Depends(get_db)):

    return user_repository.get_user(user_id, response, db)


@router.get("/{book_id}")
async def get_user(book_id: int):
    return book_id
