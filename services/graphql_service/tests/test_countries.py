import pytest
from app.models import Country
from app.schemas.graphene_schema import graphene_schema


async def gql(query: str, db_session, variables=None):
    result = await graphene_schema.execute_async(
        query, variable_values=variables, context_value={"session": db_session}
    )
    return result


@pytest.mark.asyncio
# @mock.patch("app.schemas.graphene_schema.notify_email_service")
async def test_add_country(db_session, monkeypatch):
    monkeypatch.setattr(
        "app.notification.email_service.notify_email_service",
        lambda *args, **kwargs: None,
    )

    query = """
        mutation AddCountry($input: AddCountryInput!) {
            addCountry(input: $input) {
                success
                message
            }
        }
    """

    variables = {
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

    result = await gql(query, db_session, variables)

    assert result.errors is None
    assert result.data["addCountry"]["success"] is True


@pytest.mark.asyncio
async def test_get_country(db_session):
    c = Country(name="Japan", alpha2_code="JP", capital="Tokyo")
    db_session.add(c)
    await db_session.commit()

    query = """
        query {
            getCountry(countryCode: "JP") {
                name
                capital
            }
        }
    """

    result = await gql(query, db_session)

    assert result.errors is None
    assert result.data["getCountry"]["name"] == "Japan"


@pytest.mark.asyncio
async def test_countries_list(db_session):
    c1 = Country(name="India", alpha2_code="IN")
    c2 = Country(name="Nepal", alpha2_code="NP")
    db_session.add_all([c1, c2])
    await db_session.commit()

    query = """
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

    result = await gql(query, db_session)

    assert result.errors is None
    assert len(result.data["countriesList"]) == 1


@pytest.mark.asyncio
async def test_nearby_countries(db_session):
    india = Country(name="India", alpha2_code="IN", latitude=20.5937, longitude=78.9629)
    dubai = Country(name="UAE", alpha2_code="AE", latitude=25.2048, longitude=55.2708)

    db_session.add_all([india, dubai])
    await db_session.commit()

    query = """
        query {
            nearbyCountries(latitude: 20.0, longitude: 78.0, radiusKm: 1000) {
                name
            }
        }
    """

    result = await gql(query, db_session)

    names = [c["name"] for c in result.data["nearbyCountries"]]

    assert "India" in names
    assert "UAE" not in names
