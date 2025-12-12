from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Country


async def check_country_exists(db: AsyncSession, alpha2_code: str) -> bool:
    stmt = select(Country).where(Country.alpha2_code == alpha2_code)
    result = await db.execute(stmt)
    return result.scalars().first() is not None
