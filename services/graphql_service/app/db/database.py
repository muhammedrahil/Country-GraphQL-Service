from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import asynccontextmanager

from app.settings import settings

engine = create_async_engine(
    settings.database_url,
    echo=False,
    pool_size=10,  # Number of connections to maintain in the pool
    max_overflow=5,  # Number of connections to allow in overflow
    pool_timeout=30,  # Number of seconds to wait before giving up on getting a connection
    pool_recycle=1800,  # Number of seconds after which a connection is automatically recycled
    pool_pre_ping=True,  # Enable the connection pool "pre-ping" feature
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=True,
    autocommit=False,
    expire_on_commit=False,
)
Base = declarative_base()


async def get_db():
    """
    Provides a database session, yielding it for use within a request context.
    After the request, the session is closed to free up resources.
    """
    async with SessionLocal() as db:  # Use async session context manager
        try:
            yield db  # Yield the async session to be used in a route or service
        finally:
            await db.close()


@asynccontextmanager
async def get_session():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
