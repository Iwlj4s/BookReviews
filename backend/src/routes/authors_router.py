from fastapi import Depends, APIRouter, Response

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import shema, models
from src.database.database import get_db

from src.helpers.general_helper import CheckHTTP404NotFound

from src.DAO.general_dao import GeneralDAO

authors_router = APIRouter(
    prefix="/api/authors",
    tags=["authors"]
)


@authors_router.get("/author/{author_id}", tags=["authors"])
async def get_author(author_id: int,
                     db: AsyncSession = Depends(get_db)):
    author = await GeneralDAO.get_item_by_id(db=db, item=models.Author, item_id=int(author_id))
    return author


@authors_router.get("/authors_list", tags=["authors"])
async def get_authors(db: AsyncSession = Depends(get_db)):
    authors = await GeneralDAO.get_all_items(db=db, item=models.Author)
    return authors
