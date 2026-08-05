from pydantic import BaseModel


class Country(BaseModel):
    name: str
    countryCode: str

class City(BaseModel):
    name: str

class Location(BaseModel):
    longitude: str
    latitude: str

class Venue(BaseModel):
    name: str
    type: str
    id: str
    city: City
    country: Country
    location: Location
