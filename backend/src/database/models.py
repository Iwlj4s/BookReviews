from sqlalchemy import Column, String, Text, text,  Integer, Boolean, ForeignKey
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


class UserReview(Base):
    __tablename__ = 'user_reviews'
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    book_review: Mapped[str] = mapped_column(String, ForeignKey("users.id"))


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    book_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    book_author: Mapped[str] = mapped_column(String, nullable=False, index=True)
    book_description: Mapped[str] = mapped_column(String, nullable=False, index=True)
