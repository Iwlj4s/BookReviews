from typing import Optional

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from backend.src.database.database import engine, Base
from backend.src.database import models, shema

from backend.src.DAO.general_dao import GeneralDAO

from backend.src.database.database import get_db
from backend.src.repository.reviews_repository import get_all_reviews

from backend.src.routes.admin_router import admin_router
from backend.src.routes.users_router import users_router
from backend.src.routes.books_router import books_router
from backend.src.routes.authors_router import authors_router
from backend.src.routes.reviews_router import reviews_router


app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://87.228.10.180"
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


app.include_router(admin_router, prefix="/api/admin")
app.include_router(users_router, prefix="/api/users")
app.include_router(reviews_router, prefix="/api/reviews")
app.include_router(authors_router, prefix="/api/authors")
app.include_router(books_router, prefix="/api/books")


@app.get("/api/", response_model=Optional[shema.ReviewOut])
async def home_page(db: AsyncSession = Depends(get_db)):
    review = await GeneralDAO.get_last_review_with_relations(db=db)
    return review
