from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.src.database.database import engine
from backend.src.router import router

from backend.src.database import models


app = FastAPI()

app.include_router(router)

models.Base.metadata.create_all(engine)

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
