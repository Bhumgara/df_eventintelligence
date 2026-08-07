from typing import Optional

from pydantic import BaseModel

class EventRecord(BaseModel):
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
