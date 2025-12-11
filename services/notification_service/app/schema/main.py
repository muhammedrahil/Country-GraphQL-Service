from pydantic import BaseModel


class CountryNotification(BaseModel):
    """Schema for country notification."""

    name: str
    alpha2_code: str
    capital: str | None = None
    region: str | None = None
    population: int | None = None
    created_at: str
