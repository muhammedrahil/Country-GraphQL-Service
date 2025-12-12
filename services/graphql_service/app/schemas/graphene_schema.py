import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Country


class CountryType(SQLAlchemyObjectType):
    class Meta:
        model = Country
        # only_fields = ('id', 'alpha2_code', 'name')


class Query(graphene.ObjectType):
    countries = graphene.List(CountryType)
    country = graphene.Field(CountryType, country_code=graphene.String(required=True))

    async def resolve_country(self, info, country_code: str) -> CountryType | None:
        """Get a single country by code."""
        db: AsyncSession = info.context["db"]
        try:
            # Use async query execution with proper result handling
            stmt = select(Country).where(Country.alpha2_code == country_code)
            result = await db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            print(f"Error resolving country: {e}")
            return None

    async def resolve_countries(self, info, **kwargs) -> list[CountryType]:
        """List all countries."""
        db: AsyncSession = info.context["db"]
        try:
            stmt = select(Country)
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            print(f"Error resolving countries: {e}")
            return []


graphene_schema = graphene.Schema(query=Query)
