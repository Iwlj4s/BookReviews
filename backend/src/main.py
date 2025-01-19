from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database.database import engine, Base
from backend.src.database import models

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


@app.get("/")
@app.get("/home")
async def home_page(db: AsyncSession = Depends(get_db)):
    review = await GeneralDAO.get_last_record(db=db, item=models.Review)
    return review
