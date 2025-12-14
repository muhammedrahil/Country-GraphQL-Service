import asyncio
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.db.database import get_session
from app.models import Country
from app.graphene_schema_input.countries import AddCountryInput
from app.notification.email_service import notify_email_service
from app.services.countries import (
    add_country,
    countries_curser_pagination_list,
    countries_offset_pagination_list,
    get_country,
    nearby_countries,
)
from app.validation.countries import check_country_exists


class CountryType(SQLAlchemyObjectType):
    class Meta:
        model = Country
        interfaces = (graphene.relay.Node,)


class CountryConnection(graphene.relay.Connection):
    """Pagination for countries."""

    class Meta:
        node = CountryType

    total_count = graphene.Int()

    def resolve_total_count(self, info):
        return len(self.iterable) if hasattr(self, "iterable") else 0


class GetCountryQuery(graphene.ObjectType):
    countries_offset_list = graphene.List(
        CountryType,
        limit=graphene.Int(default_value=10),
        offset=graphene.Int(default_value=0),
    )

    countries_curser_list = graphene.relay.ConnectionField(CountryConnection)

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
        # Use session from context if available (for testing), otherwise create new session
        if hasattr(info.context, "get") and "session" in info.context:
            db = info.context["session"]
            return await get_country(db=db, country_code=country_code)
        else:
            async with get_session() as db:
                return await get_country(db=db, country_code=country_code)

    async def resolve_countries_offset_list(
        self, info, limit: int = 0, offset: int = 0
    ) -> list[CountryType]:
        """List all countries."""
        # Use session from context if available (for testing), otherwise create new session
        if hasattr(info.context, "get") and "session" in info.context:
            db = info.context["session"]
            return await countries_offset_pagination_list(
                db=db, limit=limit, offset=offset
            )
        else:
            async with get_session() as db:
                return await countries_offset_pagination_list(
                    db=db, limit=limit, offset=offset
                )

    async def resolve_countries_curser_list(self, info, **kwargs) -> list[CountryType]:
        """List all countries."""
        # Use session from context if available (for testing), otherwise create new session
        if hasattr(info.context, "get") and "session" in info.context:
            db = info.context["session"]
            return await countries_curser_pagination_list(db=db)
        else:
            async with get_session() as db:
                return await countries_curser_pagination_list(db=db)

    async def resolve_nearby_countries(
        self, info, latitude: float, longitude: float, radius_km: float = 500
    ):
        # Use session from context if available (for testing), otherwise create new session
        if hasattr(info.context, "get") and "session" in info.context:
            db = info.context["session"]
            return await nearby_countries(
                db=db, latitude=latitude, longitude=longitude, radius_km=radius_km
            )
        else:
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
        # Use session from context if available (for testing), otherwise create new session
        if hasattr(info.context, "get") and "session" in info.context:
            db = info.context["session"]
            existing = await check_country_exists(db=db, alpha2_code=input.alpha2_code)
            if existing:
                return AddCountryMutation(
                    success=False,
                    message=f"Country with code {input.alpha2_code} already exists",
                )
            country = await add_country(db=db, input=input)
            asyncio.create_task(
                notify_email_service(
                    country_data={
                        "name": country.name,
                        "alpha2_code": country.alpha2_code,
                        "capital": country.capital,
                        "region": country.region,
                        "population": country.population,
                        "created_at": country.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )
            )
            return AddCountryMutation(
                success=True, message="Country added successfully"
            )
        else:
            async with get_session() as db:
                existing = await check_country_exists(
                    db=db, alpha2_code=input.alpha2_code
                )
                if existing:
                    return AddCountryMutation(
                        success=False,
                        message=f"Country with code {input.alpha2_code} already exists",
                    )
                country = await add_country(db=db, input=input)
                asyncio.create_task(
                    notify_email_service(
                        country_data={
                            "name": country.name,
                            "alpha2_code": country.alpha2_code,
                            "capital": country.capital,
                            "region": country.region,
                            "population": country.population,
                            "created_at": country.created_at.strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                        }
                    )
                )
                return AddCountryMutation(
                    success=True, message="Country added successfully"
                )


class Mutation(graphene.ObjectType):
    add_country = AddCountryMutation.Field()


graphene_schema = graphene.Schema(
    query=GetCountryQuery,
    mutation=Mutation,
)
