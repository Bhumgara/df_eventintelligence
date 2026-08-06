from pydantic import BaseModel, Field
from typing import Optional

class Venue(BaseModel):
    id: int
    name: str
    address: str
    town: str
    postcode: str
    region: str
    country: str
    phone: str
    latitude: float
    longitude: float
    type: str

class Event(BaseModel):
    id: int
    listingid: int
    isSBT: bool
    uniquelistingidentifier: str
    hascollapsedresults: bool
    countcollapsedresults: int
    eventcode: str = Field(alias='EventCode')
    eventname: str
    venue: Venue
    startdate: str
    enddate: str
    description: str
    eventvisibility: str
    link: str