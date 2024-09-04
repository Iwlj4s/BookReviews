from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.src.database.database import engine, Base

from backend.src.routes.users_router import users_router
from backend.src.routes.reviews_router import reviews_router

app = FastAPI()


@app.get("/")
async def home_page():
    return {"Hello there!"}

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def startup_event():
    await create_tables()


app.include_router(users_router)
app.include_router(reviews_router)
