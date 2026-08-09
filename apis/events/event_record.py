from typing import Optional

from pydantic import BaseModel

class TmEventRecord(BaseModel):
    name: str
    typeOfEvent: str
    id: str
    url: str
    locale: str
    startDate: str
    multipleDays: bool
    venues: list[str]
    genre_name: Optional[str]
    subgenre_name: Optional[str]

class SkEventRecord(BaseModel):
    id: int
    name: str
    eventcode: str
    startdate: str
    enddate: str
    venue_id: int
    venue_name: str
    town: str
    region: str
    postcode: str
    longitude: float
    latitude: float