from typing import Optional

from pydantic import BaseModel

class SkVenue(BaseModel):
    id: int
    name: str
    address: str
    town: str
    postcode: str
    phone: str
    description: str
    latitude: float
    longitude: float
    distance: int
    type: str