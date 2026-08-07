from apis.events.client_models.ticketmaster_event_model import TmEvent, TmEventLinks
from apis.events.event_record import EventRecord
from typing import Optional

class TmEventMapper:
    @staticmethod
    def map_links_to_list(linksList: Optional[TmEventLinks]) -> tuple[list[str], list[str]]:
        if not linksList:
            return ([], [])

        newVenueLinks = [link.href for link in (linksList.venues or [])]
        newAttractionLinks = [link.href for link in (linksList.attractions or [])]

        return (newVenueLinks, newAttractionLinks)

    @staticmethod
    def map_event_record_to_dict(record: EventRecord) -> dict:
        return {
            "name": record.name,
            "typeOfEvent": record.typeOfEvent,
            "id": record.id,
            "url": record.url,
            "locale": record.locale,
            "startDate": record.startDate,
            "multipleDays": record.multipleDays,
            "venues": record.venues,
            "genre_name": record.genre_name,
            "subgenre_name": record.subgenre_name
        }

    def map_event_to_record(event: TmEvent) -> EventRecord:
            return EventRecord(
                name = event.name,
                typeOfEvent = event.typeOfEvent,
                id = event.id,
                url = event.url,
                locale = event.locale,
                startDate = event.dates.start.localDate,
                multipleDays = event.dates.spanMultipleDays,
                venues = TmEventMapper.map_links_to_list(event.links)[0],
                # Only map the first classification for simplicity, more may be present
                genre_name=event.classifications[0].genre.name,
                subgenre_name=event.classifications[0].subGenre.name
            )


from apis.events.client_models.skiddle_event_model import Event as SkEvent

class SkEventMapper:
    @staticmethod
    def map_event_to_record(event: SkEvent) -> EventRecord:
        return EventRecord(
             name = event.eventname,
             typeOfEvent = event.eventcode,
             id = str(event.id),
             url = event.link,
             locale = '',
             startDate = event.startdate,
             multipleDays = event.startdate.split('T')[0] != event.enddate.split('T')[0],
             venues = [str(event.venue.id)]
        )