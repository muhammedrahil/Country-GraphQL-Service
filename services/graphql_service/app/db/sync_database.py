from sqlalchemy import create_engine
from services.graphql_service.app.settings import settings

db_url = settings.database_url
if db_url is None:
    raise ValueError("DATABASE_URL not provided!")

# Sync engine for APScheduler
sync_engine = create_engine(db_url.replace("+asyncpg", ""), echo=False, future=True)
