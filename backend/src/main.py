from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.src.database.database import engine
from backend.src.router import router

from backend.src.database import models
from backend.src.database.database import engine, Base


app = FastAPI()

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
    async with engine.begin() as conn:  # Используйте асинхронный контекстный менеджер
        await conn.run_sync(Base.metadata.create_all)  # Создайте все таблицы


@app.on_event("startup")
async def startup_event():
    await create_tables()  # Запустите асинхронную функцию при старте приложения

# Подключите маршрутизатор
from backend.src.router import router
app.include_router(router)
