from apis.events.client_models.event_model import Event, EventLinks
from apis.events.event_record import EventRecord
from typing import Optional

class EventMapper:
    @staticmethod
    def map_links_to_list(linksList: Optional[EventLinks]) -> tuple[list[str], list[str]]:
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
            "venues": record.venues
        }

    def map_event_to_record(self, event: Event) -> EventRecord:
            return EventRecord(
                name = event.name,
                typeOfEvent = event.typeOfEvent,
                id = event.id,
                url = event.url,
                locale = event.locale,
                startDate = event.dates.start.localDate,
                multipleDays = event.dates.spanMultipleDays,
                venues = self.map_links_to_list(event.links)[0]
            )