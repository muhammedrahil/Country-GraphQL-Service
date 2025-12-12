import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.db.database import get_session
from app.models import Country
from app.resolvers.countries import (
    countries_pagination_list,
    get_country,
    nearby_countries,
)


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
            return await get_country(db=db, country_code=country_code)

    async def resolve_countries_list(self, info, **kwargs) -> list[CountryType]:
        """List all countries."""
        limit = kwargs.get("limit", 0)
        offset = kwargs.get("offset", 0)
        async with get_session() as db:
            return await countries_pagination_list(db=db, limit=limit, offset=offset)

    async def resolve_nearby_countries(
        self, info, latitude: float, longitude: float, radius_km: float = 500
    ):
        async with get_session() as db:
            return await nearby_countries(
                db=db, latitude=latitude, longitude=longitude, radius_km=radius_km
            )


graphene_schema = graphene.Schema(query=Query)
