from typing import Optional

from pydantic import BaseModel, Field


class Country(BaseModel):
    name: str
    countryCode: str

class City(BaseModel):
    name: str

class Location(BaseModel):
    longitude: float = Field(ge=-180, le=180)
    latitude: float = Field(ge=-90, le=90)

class Venue(BaseModel):
    name: str
    type: Optional[str]
    id: str
    postalCode: str
    city: City
    country: Country
    location: Location
