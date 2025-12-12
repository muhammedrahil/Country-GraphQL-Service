import os
import sys
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.db.database import Base

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)


TEST_DB_URL = (
    "postgresql+asyncpg://postgres:Zaigo%4025@localhost:5432/country-graphql-service"
)


# Create tables per test to ensure clean state
@pytest_asyncio.fixture(autouse=True)
async def prepare_database():
    engine = create_async_engine(TEST_DB_URL, future=True, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


# Create a fresh transaction per test
@pytest_asyncio.fixture
async def db_session():
    # Create a new engine for each test to ensure isolation and avoid loop issues
    engine = create_async_engine(TEST_DB_URL, future=True, echo=False)

    async with engine.connect() as conn:
        trans = await conn.begin()  # begin outer transaction
        session = AsyncSession(bind=conn, expire_on_commit=False)

        # Override the dependency so the app uses THIS session
        from contextlib import asynccontextmanager

        @asynccontextmanager
        async def override_get_session():
            yield session

        # Patch where it is imported/used.
        import app.schemas.graphene_schema

        original_get_session = app.schemas.graphene_schema.get_session
        app.schemas.graphene_schema.get_session = override_get_session

        try:
            yield session
        finally:
            app.schemas.graphene_schema.get_session = original_get_session
            await session.close()
            await trans.rollback()  # rollback after test

    await engine.dispose()
