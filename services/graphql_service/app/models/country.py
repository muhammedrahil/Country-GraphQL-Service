from sqlalchemy import Column, Float, Integer, String, JSON, Boolean

from services.graphql_service.app.models.basemodel import BaseModel


class Country(BaseModel):
    """SQLAlchemy model representing country data.

    Stores comprehensive country information including names, codes,
    geographic data, population, flags, and other metadata.
    """

    __tablename__ = "countries"

    name = Column(String(255), nullable=False, index=True)
    native_name = Column(String(255))
    alpha2_code = Column(String(2), unique=True, index=True)
    alpha3_code = Column(String(3), unique=True, index=True)
    capital = Column(String(255))
    region = Column(String(100), index=True)
    subregion = Column(String(100))
    population = Column(Integer)
    area = Column(Float)
    latitude = Column(Float, index=True)
    longitude = Column(Float, index=True)
    timezones = Column(JSON)
    borders = Column(JSON)
    currencies = Column(JSON)
    languages = Column(JSON)
    flag_svg = Column(String(500))
    flag_png = Column(String(500))
    independent = Column(Boolean)

    def __repr__(self):
        return f"<Country(name={self.name}, code={self.alpha2_code})>"
