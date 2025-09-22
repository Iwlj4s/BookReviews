from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from dotenv import load_dotenv

from backend.config import settings

load_dotenv()

# SQLITE #
# SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# PostgreSQL #
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL_POSTGRE

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  
    future=True,
    pool_pre_ping=True,  
    pool_recycle=300,
)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()