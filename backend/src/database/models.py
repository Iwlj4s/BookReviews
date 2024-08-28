from sqlalchemy import Column, String, Integer, ForeignKey

from backend.src.database.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)


class UserReview(Base):
    __tablename__ = 'user_reviews'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    book_review = Column(String, ForeignKey('books.id'))


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    book_name = Column(String, index=True)
    book_author = Column(String, index=True)
    book_description = Column(String, index=True)
