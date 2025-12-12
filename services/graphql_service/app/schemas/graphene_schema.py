import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.db.database import get_session
from app.models import Country
from app.graphene_schema_input.countries import AddCountryInput
from app.services.countries import (
    add_country,
    countries_pagination_list,
    get_country,
    nearby_countries,
)
from app.validation.countries import check_country_exists


class CountryType(SQLAlchemyObjectType):
    class Meta:
        model = Country


class GetCountryQuery(graphene.ObjectType):
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


class AddCountryMutation(graphene.Mutation):
    """Mutation to add a new country."""

    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        input = AddCountryInput(required=True)

    async def mutate(self, info, input: AddCountryInput):
        async with get_session() as db:
            existing = await check_country_exists(db=db, alpha2_code=input.alpha2_code)
            if existing:
                return AddCountryMutation(
                    success=False,
                    message=f"Country with code {input.alpha2_code} already exists",
                )
            await add_country(db=db, input=input)
            return AddCountryMutation(
                success=True, message="Country added successfully"
            )


class Mutation(graphene.ObjectType):
    add_country = AddCountryMutation.Field()


graphene_schema = graphene.Schema(query=GetCountryQuery, mutation=Mutation)
