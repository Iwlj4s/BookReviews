from typing import List, Optional
from enum import Enum

from sqlalchemy import Column, String, Text, text, Integer, Boolean, ForeignKey, DateTime, func, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.database.database import Base


class ActionType(str, Enum):
    BLOCK_USER = "BLOCK_USER"
    DELETE_REVIEW = "DELETE_REVIEW"
    WARN_USER = "WARN_USER"


class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String)

    profile_picture: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    registration_date: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text("True"), nullable=False)
    is_user: Mapped[bool] = mapped_column(default=True, server_default=text("True"), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text("False"), nullable=False)

    warnings: Mapped[int] = mapped_column(default=0, server_default=text("0"), nullable=False)

    reviews: Mapped[List["Review"]] = relationship("Review",
                                                   back_populates="user",
                                                   lazy="selectin")
    ratings: Mapped[List["BookRating"]] = relationship("BookRating",
                                                       back_populates="user",
                                                       lazy="selectin")
    warnings_received: Mapped[List["Warning"]] = relationship("Warning",
                                                              foreign_keys="Warning.user_id",
                                                              back_populates="user",
                                                              lazy="selectin")
    blocks_received: Mapped[List["BlockedUser"]] = relationship("BlockedUser",
                                                                foreign_keys="BlockedUser.user_id",
                                                                back_populates="user",
                                                                lazy="selectin")
    admin_actions_received: Mapped[List["AdminAction"]] = relationship("AdminAction",
                                                                       foreign_keys="AdminAction.target_user_id",
                                                                       back_populates="target_user",
                                                                       lazy="selectin")


class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)

    books: Mapped[List["Book"]] = relationship("Book", back_populates="author", lazy="selectin")
    biography: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    book_cover: Mapped[str] = mapped_column(String, nullable=False, index=True)
    book_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False, index=True)
    book_description: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    book_average_rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    book_publication_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    author: Mapped["Author"] = relationship("Author", back_populates="books", lazy="selectin")

    reviews: Mapped[List["Review"]] = relationship(
        "Review",
        back_populates="book",
        foreign_keys="Review.reviewed_book_id",
        lazy="selectin"
    )

    ratings: Mapped[List["BookRating"]] = relationship(
        "BookRating",
        back_populates="book",
        lazy="selectin"
    )

    external_ratings: Mapped[List["ExternalRating"]] = relationship(
        "ExternalRating",
        back_populates="book",
        lazy="selectin"
    )


class BookRating(Base):
    __tablename__ = 'book_ratings'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    date: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)
    book: Mapped["Book"] = relationship("Book", back_populates="ratings")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="ratings")


class ExternalRating(Base):
    __tablename__ = 'external_ratings'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    source: Mapped[str] = mapped_column(String, nullable=False)
    external_rating: Mapped[float] = mapped_column(Float, nullable=False)
    external_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)

    book: Mapped["Book"] = relationship("Book", back_populates="external_ratings")


class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    reviewed_book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False, index=True)
    reviewed_book_author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False, index=True)

    reviewed_book_cover: Mapped[str] = mapped_column(ForeignKey("books.book_cover"), nullable=False, index=True)
    rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    review_title: Mapped[str] = mapped_column(String, nullable=True, index=True, )
    review_body: Mapped[str] = mapped_column(Text, nullable=False, index=True, )

    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    user: Mapped["User"] = relationship("User", back_populates="reviews", lazy="selectin")

    book: Mapped["Book"] = relationship(
        "Book",
        back_populates="reviews",
        foreign_keys=[reviewed_book_id],
        lazy="selectin"
    )

    author: Mapped["Author"] = relationship(
        "Author",
        foreign_keys=[reviewed_book_author_id],
        lazy="selectin"
    )


class AdminAction(Base):
    __tablename__ = 'admin_actions'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    action_type: Mapped[str] = mapped_column(String, nullable=False)
    action_date: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    reason: Mapped[str] = mapped_column(String, nullable=False)
    target_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    performed_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    target_user: Mapped["User"] = relationship("User", foreign_keys=[target_user_id],
                                               back_populates="admin_actions_received")
    performed_by: Mapped["User"] = relationship("User", foreign_keys=[performed_by_id])


class Warning(Base):
    __tablename__ = 'warnings'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    severity: Mapped[str] = mapped_column(String, nullable=False)
    message: Mapped[str] = mapped_column(String, nullable=False)
    expiration_date: Mapped[Optional[DateTime]] = mapped_column(DateTime, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, server_default=text("0"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    admin_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship("User", foreign_keys=[user_id], back_populates="warnings_received")
    admin: Mapped["User"] = relationship("User", foreign_keys=[admin_id])


class BlockedUser(Base):
    __tablename__ = 'blocked_users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    block_start: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    block_end: Mapped[Optional[DateTime]] = mapped_column(DateTime, nullable=True)
    is_permanent: Mapped[bool] = mapped_column(Boolean, server_default=text("0"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    admin_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship("User", foreign_keys=[user_id], back_populates="blocks_received")
    admin: Mapped["User"] = relationship("User", foreign_keys=[admin_id])


class DeletedReview(Base):
    __tablename__ = 'deleted_reviews'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    deletion_date: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    original_content: Mapped[str] = mapped_column(Text, nullable=False)
    reason: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)
    book_name: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)
    author_name: Mapped[str] = mapped_column(String, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user_name: Mapped[str] = mapped_column(String, nullable=False)

    review_id: Mapped[int] = mapped_column(ForeignKey("reviews.id"), nullable=False, unique=True)
    admin_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    review: Mapped["Review"] = relationship(
        "Review",
        foreign_keys=[review_id]
    )
    admin: Mapped["User"] = relationship("User", foreign_keys=[admin_id])
    book: Mapped["Book"] = relationship("Book", foreign_keys=[book_id])
    author: Mapped["Author"] = relationship("Author", foreign_keys=[author_id])
    user: Mapped["User"] = relationship("User", foreign_keys=[user_id])
