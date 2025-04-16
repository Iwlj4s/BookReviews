from fastapi import Query
from pydantic import BaseModel, Field, validator
from typing import Union


# User #
class User(BaseModel):
    name: Union[str, None] = Field(default=None, min_length=3, title="Имя пользователя")
    email: Union[str, None] = Field(default=None, title="Эл.почта пользователя")
    password: Union[str, None] = Field(default=None, min_length=4, title="Пароль пользователя")


class UserSignIn(BaseModel):
    email: Union[str] = Field(default=None, title="Эл.почта пользователя")
    password: Union[str] = Field(default=None, min_length=4, title="Пароль пользователя")


class UserSignUp(BaseModel):
    name: Union[str] = Field(default=None, min_length=3, title="Имя пользователя")
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

    @validator('name')
    def capitalize_name(cls, v):
        if v:
            return v.title()
        return v


# Book #
class Book(BaseModel):
    book_author_name: Union[str, None] = Field(default=None, title="Имя автора")
    book_name: Union[str, None] = Field(default=None, title="Название книги")
    book_description: Union[str, None] = Field(default=None, title="Описание книги")

    @validator('book_name')
    def capitalize_name(cls, v):
        if v:
            return v.capitalize()
        return v


# Newsletter for all users #
class NewsletterForAllUsers(BaseModel):
    mail_theme: Union[str, None] = Field(default=None, title="Тема письма")
    mail_body: Union[str, None] = Field(default=None, title="Тело письма")


class NewsLetterForUser(BaseModel):
    receiver_email: Union[str, None] = Field(default=None, title="Id пользователя, которому отправляется письмо")
    mail_theme: Union[str, None] = Field(default=None, title="Тема письма")
    mail_body: Union[str, None] = Field(default=None, title="Тело письма")


# Token #
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None
    id: int
