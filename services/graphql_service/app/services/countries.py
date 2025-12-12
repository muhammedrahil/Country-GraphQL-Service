from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Country
from geopy.distance import distance
from app.graphene_schema_input.countries import AddCountryInput


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


async def add_country(db: AsyncSession, input: AddCountryInput):
    country = Country(
        name=input.name,
        alpha2_code=input.alpha2_code,
        alpha3_code=input.alpha3_code,
        capital=input.capital,
        region=input.region,
        subregion=input.subregion,
        population=input.population,
        area=input.area,
        latitude=input.latitude,
        longitude=input.longitude,
        calling_codes=input.calling_codes,
        timezones=input.timezones,
        currencies=input.currencies,
        languages=input.languages,
        flag_svg=input.flag_svg,
        flag_png=input.flag_png,
        independent=input.independent,
    )
    db.add(country)
    await db.commit()
    await db.refresh(country)
    return country
