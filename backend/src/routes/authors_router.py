from fastapi import Depends, APIRouter, Response

from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database import shema, models
from backend.src.database.database import get_db

from backend.src.helpers.general_helper import CheckHTTP404NotFound

from backend.src.DAO.general_dao import GeneralDAO

authors_router = APIRouter(
    prefix="/book_reviews/api/authors",
    tags=["authors"]
)


@authors_router.get("/author/{author_id}", tags=["authors"])
async def get_author(author_id: int,
                     db: AsyncSession = Depends(get_db)):
    author = await GeneralDAO.get_item_by_id(db=db, item=models.Author, item_id=int(author_id))
    CheckHTTP404NotFound(founding_item=author, text="Автор не найден")
    return author


@authors_router.get("/authors_list", tags=["authors"])
async def get_authors(db: AsyncSession = Depends(get_db)):
    authors = await GeneralDAO.get_all_items(db=db, item=models.Author)
    CheckHTTP404NotFound(founding_item=authors, text="Авторы не найден")
    return authors
