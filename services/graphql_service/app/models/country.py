from sqlalchemy import Column, Float, Integer, String, Text

from services.graphql_service.app.models.basemodel import BaseModel


class Country(BaseModel):
    """Country model storing comprehensive country information."""

    __tablename__ = "countries"

    name = Column(String(255), nullable=False, index=True)
    official_name = Column(String(255))
    alpha2_code = Column(String(2), unique=True, index=True)
    alpha3_code = Column(String(3), unique=True, index=True)
    capital = Column(String(255))
    region = Column(String(100), index=True)
    subregion = Column(String(100))
    population = Column(Integer)
    area = Column(Float)
    latitude = Column(Float, index=True)
    longitude = Column(Float, index=True)
    timezones = Column(Text)  # JSON string
    currencies = Column(Text)  # JSON string
    languages = Column(Text)  # JSON string
    flag_url = Column(String(500))

    def __repr__(self):
        return f"<Country(name={self.name}, code={self.alpha2_code})>"
