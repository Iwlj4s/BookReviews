from typing import List

from sqlalchemy import Column, String, Text, text, Integer, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from backend.src.database.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String)

    is_user: Mapped[bool] = mapped_column(default=True, server_default=text("True"), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text("False"), nullable=False)

    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="user", lazy="selectin")


class Review(Base):
    __tablename__ = 'reviews'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    reviewed_book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False, index=True)  # FK на Book

    reviewed_book_name: Mapped[str] = mapped_column(nullable=False, index=True)
    reviewed_book_author_name: Mapped[str] = mapped_column(nullable=False, index=True)

    review_title: Mapped[str] = mapped_column(String, nullable=True, index=True,)
    review_body: Mapped[str] = mapped_column(Text, nullable=False, index=True,)

    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    user: Mapped["User"] = relationship("User", back_populates="reviews", lazy="selectin")


class Author(Base):
    __tablename__ = 'authors'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)

    books: Mapped[List["Book"]] = relationship("Book", back_populates="author", lazy="selectin")


# TODO: Think about parse https://www.litres.ru/search/ for take book cover img
class Book(Base):
    __tablename__ = 'books'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    book_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False, index=True)
    book_description: Mapped[str] = mapped_column(Text, nullable=False, index=True)

    author: Mapped["Author"] = relationship("Author", back_populates="books", lazy="selectin")
