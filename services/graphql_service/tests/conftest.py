import os
import sys
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from app.db.database import Base  # noqa: E402

TEST_DB_URL = (
    "postgresql+asyncpg://postgres:Zaigo%4025@localhost:5432/country-graphql-service"
)


@pytest_asyncio.fixture
async def async_engine():
    engine = create_async_engine(TEST_DB_URL, future=True)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def reset_database(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest_asyncio.fixture
async def db_session(async_engine, reset_database):
    async_session = sessionmaker(
        async_engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        yield session
