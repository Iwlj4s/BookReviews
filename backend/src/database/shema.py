from fastapi import Query
from pydantic import BaseModel, Field
from typing import Union


# User #
class User(BaseModel):
    name: Union[str, None] = Field(default=None, min_length=3, title="Имя пользователя")
    email: Union[str, None] = Field(default=None, title="Эл.почта пользователя")
    password: Union[str, None] = Field(default=None, min_length=4, title="Пароль пользователя")


class UserSignIn(BaseModel):
    email: Union[str] = Field(default=None, title="Эл.почта пользователя")
    password: Union[str] = Field(default=None, min_length=4, title="Пароль пользователя")


# Review #
class Review(BaseModel):
    reviewed_book_name: Union[str] = Field(default=None, title="Название книги, на которую написан обзор")
    reviewed_book_author_name: Union[str] = Field(default=None, title="Имя автора книги, на которую написан обзор")

    review_title: Union[str] = Field(default=None, min_length=5, title="Заголовок обзора")
    review_body: Union[str] = Field(default=None, min_length=5, title="Обзор")


class FilteredReview(BaseModel):
    reviewed_book_name: Union[str, None] = Field(default=None, title="Название книги")
    reviewed_author_name: Union[str, None] = Field(default=None, title="Имя автора")


class ChangeReview(BaseModel):
    review_title: Union[str, None] = Field(default=None, min_length=5, title="Заголовок обзора")
    review_body: Union[str, None] = Field(default=None, min_length=5, title="Обзор")


# Author #
class Author(BaseModel):
    name: Union[str, None] = Field(default=None, title="Имя автора")


# Book #
class Book(BaseModel):
    book_name: Union[str, None] = Field(default=None, title="Название книги")
    book_author_name: Union[str, None] = Field(default=None, title="Имя автора")
    book_description: Union[str, None] = Field(default=None, title="Описание книги")


# Token #
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None
    id: int