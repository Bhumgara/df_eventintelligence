from pydantic import BaseModel


class VenueRecord(BaseModel):
    name: str
    type: str
    id: str
    city: str
    country: str
    longitude: float
    latitude: float