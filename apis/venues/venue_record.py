from pydantic import BaseModel


class TmVenueRecord(BaseModel):
    name: str
    type: str
    id: str
    city: str
    country: str
    postalCode: str
    longitude: float
    latitude: float

class SkVenueRecord(BaseModel):
    id: int
    name: str
    type: str
    town: str
    postcode: str
    longitude: float
    latitude: float
