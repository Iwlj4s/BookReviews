from fastapi import Depends, APIRouter, Response
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.database import shema
from backend.src.database.database import get_db

books_router = APIRouter(
    prefix="/book_reviews/books",
    tags=["books"]
)


@books_router.get("/{book_id}")
async def get_user(book_id: int):
    return book_id