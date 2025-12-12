from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Country
from geopy.distance import distance


async def get_country(db: AsyncSession, country_code: str) -> Country:
    """Get a single country by code."""
    try:
        stmt = select(Country).where(Country.alpha2_code == country_code)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    except Exception as e:
        print(f"Error resolving country: {e}")
        return None


async def countries_pagination_list(
    db: AsyncSession, limit: int = 0, offset: int = 0
) -> list[Country]:
    """List all countries."""
    try:
        stmt = select(Country).limit(limit).offset(offset)
        result = await db.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        print(f"Error resolving countries_list: {e}")
        return []


async def nearby_countries(
    db: AsyncSession, latitude: float, longitude: float, radius_km: float = 500
):
    nearby = []
    result = await db.execute(select(Country))
    countries = result.scalars().all()

    for c in countries:
        if c.latitude is None or c.longitude is None:
            continue

        # geopy distance
        dist_km = distance((latitude, longitude), (c.latitude, c.longitude)).km

        if dist_km <= radius_km:
            nearby.append(c)

    return nearby
