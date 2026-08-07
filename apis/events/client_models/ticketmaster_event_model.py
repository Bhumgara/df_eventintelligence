from pydantic import BaseModel, Field
from typing import Optional

class LinksHref(BaseModel):
    href: str

class TmEventLinks(BaseModel):
    self: LinksHref
    attractions: Optional[list[LinksHref]] = None
    venues: Optional[list[LinksHref]] = None

class StartDate(BaseModel):
    localDate: str
    localTime: Optional[str] = None
    dateTime: Optional[str] = None
    noSpecificTime: bool

class Dates(BaseModel):
    start: StartDate
    timezone: str
    spanMultipleDays: bool

class Genre(BaseModel):
    name: Optional[str]

class SubGenre(BaseModel):
    name: Optional[str]

class Classification(BaseModel):
    genre: Genre
    subGenre: SubGenre

class TmEvent(BaseModel):
    name: str
    typeOfEvent: str  = Field(default=None, alias="type")
    id: str
    url: str
    locale: str
    dates: Dates
    links: Optional[TmEventLinks]  = Field(default=None, alias="_links")
    classifications: list[Classification]
