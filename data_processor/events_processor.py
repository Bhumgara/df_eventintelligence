from typing import Any

from pandas import DataFrame
from pydantic import ValidationError

from apis.events.event_record import EventRecord
from apis.events.events_mapper import EventMapper
from apis.events.client_models.event_model import Event

class EventsProcessor:

    def build_events_dataframe(events: list[EventRecord]) -> DataFrame:
        return DataFrame(
                [EventMapper.map_record_to_dict(ev) for ev in events]
            )

    def validate_events(event_response) -> tuple[list[EventRecord], list[dict[Any, str]]]:
        valid_events = []
        invalid_events = []

        for event in event_response:
            try:
                print(event_response)
                valid_events.append(EventMapper.map_event_to_record(Event(**event_response)))
            except ValidationError as e:
                # print(e)
                invalid_events.append({"events": event, "error": str(e)})

        if len(valid_events) == 0:
                raise Exception('No events match the schema.')
    
        return valid_events, invalid_events

