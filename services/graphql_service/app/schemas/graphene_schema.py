import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from sqlalchemy import select
from geopy.distance import distance
from app.db.database import get_session
from app.models import Country


class CountryType(SQLAlchemyObjectType):
    class Meta:
        model = Country
        # only_fields = ('id', 'alpha2_code', 'name')


class Query(graphene.ObjectType):
    countries_list = graphene.List(
        CountryType,
        limit=graphene.Int(default_value=10),
        offset=graphene.Int(default_value=0),
    )

    get_country = graphene.Field(
        CountryType, country_code=graphene.String(required=True)
    )

    nearby_countries = graphene.List(
        CountryType,
        latitude=graphene.Float(required=True),
        longitude=graphene.Float(required=True),
        radius_km=graphene.Float(default_value=500),
    )

    async def resolve_get_country(self, info, country_code: str) -> CountryType | None:
        """Get a single country by code."""
        async with get_session() as db:
            try:
                # Use async query execution with proper result handling
                stmt = select(Country).where(Country.alpha2_code == country_code)
                result = await db.execute(stmt)
                return result.scalar_one_or_none()
            except Exception as e:
                print(f"Error resolving country: {e}")
                return None

    async def resolve_countries_list(self, info, **kwargs) -> list[CountryType]:
        """List all countries."""
        limit = kwargs.get("limit", 0)
        offset = kwargs.get("offset", 0)
        async with get_session() as db:
            try:
                stmt = select(Country).limit(limit).offset(offset)
                result = await db.execute(stmt)
                return result.scalars().all()
            except Exception as e:
                print(f"Error resolving countries_list: {e}")
                return []

    async def resolve_nearby_countries(self, info, latitude, longitude, radius_km):
        # Fetch all countries
        nearby = []
        async with get_session() as db:
            result = await db.execute(select(Country))
            countries = result.scalars().all()

            for c in countries:
                # Skip invalid coordinates
                if c.latitude is None or c.longitude is None:
                    continue

                # geopy distance
                dist_km = distance((latitude, longitude), (c.latitude, c.longitude)).km

                if dist_km <= radius_km:
                    nearby.append(c)

            return nearby


graphene_schema = graphene.Schema(query=Query)
