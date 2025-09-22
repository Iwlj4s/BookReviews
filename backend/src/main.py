from typing import Optional

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from sqlalchemy import text

from backend.src.database.database import engine, Base
from backend.src.database import models, shema

from backend.src.DAO.general_dao import GeneralDAO

from backend.src.database.database import get_db
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
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)


async def create_tables():
    try:
        async with engine.begin() as conn:
            # Is tables already exist?
            result = await conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'users'
                );
            """))
            table_exists = result.scalar()
            
            if not table_exists:
                await conn.run_sync(Base.metadata.create_all)
                print("Tables created")
            else:
                print("Tables already exist")
    except Exception as e:
        print(f"Error: {e}")


@app.on_event("startup")
async def startup_event():
    import asyncio

    await asyncio.sleep(2)  
    await create_tables()



app.include_router(admin_router)
app.include_router(users_router)
app.include_router(reviews_router)
app.include_router(authors_router)
app.include_router(books_router)


@app.get("/", response_model=Optional[shema.ReviewOut])
@app.get("/home", response_model=Optional[shema.ReviewOut])
async def home_page(db: AsyncSession = Depends(get_db)):
    review = await GeneralDAO.get_last_review_with_relations(db=db)
    return review


# git fetch origin
# git checkout -t origin/local-stable-version
# git checkout local-stable-version

# If you use PostgreSQL - start server
# uvicorn backend.src.main:app --reload
# Download redis, start redis server then celery -A backend.celery.celery_app worker --loglevel=info
# cd frontend then npm run dev