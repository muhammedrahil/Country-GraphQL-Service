import pytest
import pytest_asyncio
from app.models import Country
from app.schemas.graphene_schema import graphene_schema


async def gql(query: str, db_session, variables=None):
    result = await graphene_schema.execute_async(
        query,
        variable_values=variables,
        context_value={"session": db_session},
    )
    return result


@pytest_asyncio.fixture
async def add_country():
    return """
        mutation AddCountry($input: AddCountryInput!) {
            addCountry(input: $input) {
                success
                message
            }
        }
    """


@pytest.fixture
def india_country_variables():
    return {
        "input": {
            "name": "India",
            "alpha2Code": "IN",
            "alpha3Code": "IND",
            "capital": "New Delhi",
            "region": "Asia",
            "subregion": "South Asia",
            "population": 1400000000,
            "area": 3287000,
            "latitude": 20.5937,
            "longitude": 78.9629,
            "callingCodes": ["+91"],
            "timezones": ["UTC+5:30"],
            "currencies": ["INR"],
            "languages": ["Hindi", "English"],
            "flagSvg": "svg_url",
            "flagPng": "png_url",
            "independent": True,
        }
    }


@pytest_asyncio.fixture
async def get_country():
    return """
        query {
            getCountry(countryCode: "JP") {
                name
                capital
            }
        }
    """


@pytest_asyncio.fixture
async def countries_list():
    return """
        query {
            countriesList {
                edges {
                    node {
                        name
                    }
                }
            }
        }
    """


@pytest_asyncio.fixture
async def nearby_countries():
    return """
        query {
            nearbyCountries(latitude: 20.0, longitude: 78.0, radiusKm: 1000) {
                name
            }
        }
    """


@pytest.mark.asyncio
async def test_add_country(db_session, add_country, india_country_variables):
    result = await gql(add_country, db_session, india_country_variables)
    assert result.errors is None
    assert result.data["addCountry"]["success"] is True


@pytest.mark.asyncio
async def test_get_country(db_session, get_country):
    c = Country(name="Japan", alpha2_code="JP", capital="Tokyo")
    db_session.add(c)
    await db_session.commit()

    result = await gql(get_country, db_session)

    assert result.errors is None
    assert result.data["getCountry"]["name"] == "Japan"


@pytest.mark.asyncio
async def test_countries_list(db_session, countries_list):
    c1 = Country(name="India", alpha2_code="IN")
    c2 = Country(name="Nepal", alpha2_code="NP")

    db_session.add_all([c1, c2])
    await db_session.commit()

    result = await gql(countries_list, db_session)

    assert result.errors is None
    assert len(result.data["countriesList"]["edges"]) == 2


@pytest.mark.asyncio
async def test_nearby_countries(db_session, nearby_countries):
    india = Country(
        name="India",
        alpha2_code="IN",
        latitude=20.5937,
        longitude=78.9629,
    )
    dubai = Country(
        name="UAE",
        alpha2_code="AE",
        latitude=25.2048,
        longitude=55.2708,
    )

    db_session.add_all([india, dubai])
    await db_session.commit()

    result = await gql(nearby_countries, db_session)

    names = [c["name"] for c in result.data["nearbyCountries"]]

    assert "India" in names
    assert "UAE" not in names
