from pydantic import BaseModel, Field
from typing import Optional

class LinksHref(BaseModel):
    href: str

class EventLinks(BaseModel):
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

class Event(BaseModel):
    name: str
    typeOfEvent: str  = Field(default=None, alias="type")
    id: str
    url: str
    locale: str
    dates: Dates
    links: Optional[EventLinks]  = Field(default=None, alias="_links")
