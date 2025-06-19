from typing import Optional

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.database.database import engine, Base
from src.database import models, shema

from src.DAO.general_dao import GeneralDAO

from src.database.database import get_db
from src.repository.reviews_repository import get_all_reviews

from src.routes.admin_router import admin_router
from src.routes.users_router import users_router
from src.routes.books_router import books_router
from src.routes.authors_router import authors_router
from src.routes.reviews_router import reviews_router


app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://87.228.10.180",
    "http://87.228.10.180:80",
    "http://0.0.0.0",
    "http://0.0.0.0:80"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы
    allow_headers=["*"],  # Разрешить все заголовки
)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def startup_event():
    await create_tables()

app.include_router(admin_router)
app.include_router(users_router)
app.include_router(reviews_router)
app.include_router(authors_router)
app.include_router(books_router)


@app.get("/api/", response_model=Optional[shema.ReviewOut])
async def home_page(db: AsyncSession = Depends(get_db)):
    review = await GeneralDAO.get_last_review_with_relations(db=db)

    return review
