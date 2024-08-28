from fastapi import Query
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Union


class User(BaseModel):
    name: Union[str, None] = Query(default=Field, min_length=3, title="Имя пользователя")
    email: Union[str, None] = Query(default=Field, title="Эл.почта пользователя")
    password: Union[str, None] = Query(default=Field, min_length=4, title="Пароль пользователя")


class Book(BaseModel):
    book_name: Union[str, None] = Query(default=Field)
    book_author: Union[str, None] = Query(default=Field)
    book_description: Union[str, None] = Query(default=Field)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None
    id: int
