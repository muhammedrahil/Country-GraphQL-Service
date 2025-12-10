from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.settings import settings


# The URL to the database
SQLALCHEMY_DATABASE_URL = settings.database_url

# Create the SQLAlchemy async engine that connects to the database
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,
    pool_size=10,  # Number of connections to maintain in the pool
    max_overflow=5,  # Number of connections to allow in overflow
    pool_timeout=30,  # Number of seconds to wait before giving up on getting a connection
    pool_recycle=1800,  # Number of seconds after which a connection is automatically recycled
    pool_pre_ping=True,  # Enable the connection pool "pre-ping" feature
)

# Create the session factory for creating async sessions
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=True,
    autocommit=False,
    expire_on_commit=False,
)

# Base class for your database models
Base = declarative_base()


# Dependency to get the current database session (async)
async def get_db():
    """
    Provides a database session, yielding it for use within a request context.
    After the request, the session is closed to free up resources.
    """
    async with SessionLocal() as session:  # Use async session context manager
        yield session  # Yield the async session to be used in a route or service
