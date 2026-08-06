from typing import Any

from pandas import DataFrame
from pydantic import ValidationError

from apis.events.event_record import EventRecord
from apis.events.events_mapper import TmEventMapper
from apis.events.client_models.ticketmaster_event_model import TmEvent

class EventsProcessor:

    def build_events_dataframe(events: list[EventRecord]) -> DataFrame:
        return DataFrame(
                [TmEventMapper.map_event_record_to_dict(ev) for ev in events]
            )

    def validate_events(event_response) -> tuple[list[EventRecord], list[dict[Any, str]]]:
        valid_events = []
        invalid_events = []

        for event in event_response:
            try:
                valid_events.append(TmEventMapper.map_event_to_record(TmEvent(**event)))
            except ValidationError as e:
                invalid_events.append({"events": event, "error": str(e)})

        if len(valid_events) == 0:
                raise Exception('No events match the schema.')
    
        return valid_events, invalid_events

