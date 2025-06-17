from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, Field, validator
from typing import Union, Optional, List


# Author #
class Author(BaseModel):
    id: int
    name: Union[str, None] = Field(default=None, title="Имя автора")

    @validator('name')
    def capitalize_name(cls, v):
        if v:
            return v.title()
        return v

    class Config:
        arbitrary_types_allowed = True  # Allow arbitrary types in the model
        orm_mode = True


# Book #
class Book(BaseModel):
    id: int
    book_author_name: Union[str, None] = Field(default=None, title="Имя автора")
    book_name: Union[str, None] = Field(default=None, title="Название книги")
    book_description: Union[str, None] = Field(default=None, title="Описание книги")

    @validator('book_name')
    def capitalize_name(cls, v):
        if v:
            return v.capitalize()
        return v

    class Config:
        orm_mode = True


class AddBook(BaseModel):
    book_author_name: Union[str, None] = Field(default=None, title="Имя автора")
    book_name: Union[str, None] = Field(default=None, title="Название книги")

    @validator('book_name')
    def capitalize_name(cls, v):
        if v:
            return v.capitalize()
        return v

    class Config:
        orm_mode = True


class SimpleUser(BaseModel):
    id: int
    name: Optional[str] = Field(min_length=3, title="Имя пользователя")
    email: Optional[str] = Field(title="Эл.почта пользователя")
    registration_date: Optional[datetime] = Field(title="Дата регистрации пользователя")
    warnings: int = Field(title="Предупреждения пользователя")
    is_active: bool = Field(title="Активен ли пользователь")
    is_user: bool = Field(title="Пользователь?")
    is_admin: bool = Field(title="Админ?")

    class Config:
        orm_mode = True


# Review #
class Review(BaseModel):
    id: int
    created_by: Union[int]
    user: Union[SimpleUser]

    reviewed_book_id: Union[int]
    reviewed_book_author_id: Union[int]

    reviewed_book_cover: Union[str]

    reviewed_book_id: Union[int] = Field(default=None, title="Название книги, на которую написан обзор")
    reviewed_book_author_id: Union[int] = Field(default=None, title="Имя автора книги, на которую написан обзор")

    rating: Optional[int] = Field(None, ge=1, le=5, title="Оценка книги (1-5)")

    review_title: Union[str] = Field(default=None, min_length=5, title="Заголовок обзора")
    review_body: Union[str] = Field(default=None, min_length=5, title="Обзор")

    created: Union[datetime]
    updated: Union[datetime]

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


# User #
class User(BaseModel):
    id: int
    name: Optional[str] = Field(min_length=3, title="Имя пользователя")
    email: Optional[str] = Field(title="Эл.почта пользователя")
    bio: Optional[str] = Field(title="Биография пользователя")
    profile_picture: Optional[str] = Field(title="Аватарка пользователя")
    registration_date: Optional[datetime] = Field(title="Дата регистрации пользователя")
    warnings: int = Field(title="Предупреждения пользователя")
    is_active: bool = Field(title="Активен ли пользователь")
    is_user: bool = Field(title="Пользователь?")
    is_admin: bool = Field(title="Админ?")

    reviews: List[Review] = Field(default_factory=list)

    class Config:
        orm_mode = True


class ChangeUser(BaseModel):
    name: Optional[str] = Field(min_length=3, title="Имя пользователя")
    email: Optional[str] = Field(title="Эл.почта пользователя")
    bio: Optional[str] = Field(title="Биография пользователя")
    password: Optional[str] = Field(min_length=4, title="Пароль пользователя")

    class Config:
        orm_mode = True


class ReviewHomePage(BaseModel):
    id: int
    created_by: int
    review_title: str
    review_body: str
    created: datetime
    updated: datetime
    user_name: str
    book_name: str
    author_name: str

    class Config:
        orm_mode = True


class UserSignIn(BaseModel):
    email: Union[str] = Field(default=None, title="Эл.почта пользователя")
    password: Union[str] = Field(default=None, min_length=4, title="Пароль пользователя")

    class Config:
        orm_mode = True


class UserSignUp(BaseModel):
    name: Union[str] = Field(default=None, min_length=3, title="Имя пользователя")
    email: Union[str] = Field(default=None, title="Эл.почта пользователя")
    password: Union[str] = Field(default=None, min_length=4, title="Пароль пользователя")

    class Config:
        orm_mode = True


class FilteredReview(BaseModel):
    reviewed_book_name: Union[str, None] = Field(default=None, title="Название книги")
    reviewed_author_name: Union[str, None] = Field(default=None, title="Имя автора")

    class Config:
        orm_mode = True


class ChangeReview(BaseModel):
    review_title: Union[str, None] = Field(default=None, min_length=5, title="Заголовок обзора")
    review_body: Union[str, None] = Field(default=None, min_length=5, title="Обзор")
    rating: Optional[int] = Field(None, ge=1, le=5, title="Оценка книги (1-5)")

    class Config:
        orm_mode = True


class DeletedReview(BaseModel):
    review_id: int
    original_content: str
    reason: str
    deletion_date: datetime

    book_id: int
    book_name: str

    author_id: int
    author_name: str

    user_id: int
    user_name: str

    admin_id: int
    admin_name: str

    class Config:
        orm_mode = True


# Newsletter for all users #
class NewsletterForAllUsers(BaseModel):
    mail_theme: Union[str, None] = Field(default=None, title="Тема письма")
    mail_body: Union[str, None] = Field(default=None, title="Тело письма")

    class Config:
        orm_mode = True


class NewsLetterForUser(BaseModel):
    receiver_email: Union[str, None] = Field(default=None, title="Id пользователя, которому отправляется письмо")
    mail_theme: Union[str, None] = Field(default=None, title="Тема письма")
    mail_body: Union[str, None] = Field(default=None, title="Тело письма")

    class Config:
        orm_mode = True


# Token #
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None
    id: int


# --- Pydantic схемы для вывода (response) --- #
class ReviewOut(BaseModel):
    id: int
    review_title: str
    review_body: Optional[str]
    rating: Optional[int]
    reviewed_book_id: Optional[int]
    reviewed_book_name: Optional[str]
    reviewed_book_cover: Optional[str]  # Add this
    reviewed_book_description: Optional[str]  # Add this
    reviewed_book_author_id: Optional[int]
    reviewed_book_author_name: Optional[str]
    updated: Optional[datetime]
    created: Optional[datetime]  # добавьте поле created, если нужно
    created_by: Optional[int]  # исправлено с datetime на int
    user_id: Optional[int]
    user_name: Optional[str]

    class Config:
        orm_mode = True


class ReviewWithRelationsOut(BaseModel):
    id: int
    review_title: str
    review_body: Optional[str]
    rating: Optional[int]
    reviewed_book_name: str
    reviewed_book_description: str
    reviewed_book_author_name: str
    user_name: str
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True


class BookOut(BaseModel):
    id: int
    book_name: str
    book_description: Optional[str]
    book_cover: Optional[str]
    author_id: int
    author_name: Optional[str]
    book_average_rating: Optional[float]

    class Config:
        orm_mode = True


class AuthorOut(BaseModel):
    id: int
    name: str
    biography: Optional[str]

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    is_admin: bool
    bio: Optional[str]
    reviews: List[ReviewOut] = []

    class Config:
        orm_mode = True


class ReviewCreate(BaseModel):
    reviewed_book_id: int
    reviewed_book_author_id: int
    review_title: str
    review_body: str
    rating: Optional[int] = Field(None, ge=1, le=5)

    class Config:
        orm_mode = True


class AuthorCreate(BaseModel):
    name: str

    class Config:
        orm_mode = True


class BookCreate(BaseModel):
    book_author_name: str
    book_name: str
    book_description: str

    class Config:
        orm_mode = True
