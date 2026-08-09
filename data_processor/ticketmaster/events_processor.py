from typing import Any

from pandas import DataFrame
import pandas as pd
from pydantic import ValidationError

from apis.events.event_record import TmEventRecord
from apis.events.events_mapper import TmEventMapper
from apis.events.client_models.ticketmaster_event_model import TmEvent

# class EventsProcessor:
#     def __init__(self):
#         pass

def build_events_dataframe(events: list[TmEventRecord]) -> DataFrame:
    return DataFrame(
            [TmEventMapper.map_event_record_to_dict(ev) for ev in events]
        )

def validate_events(event_response) -> tuple[list[TmEventRecord], list[dict[Any, str]]]:
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

@staticmethod
def clean_events(df: DataFrame) -> DataFrame:
    df.rename(columns={
        'id': 'event_id',
        'name': 'event_name',
        'typeOfEvent': 'event_type',
        'url': 'event_url',
        'locale': 'event_locale',
        'startDate': 'event_start_date',
        'multipleDays': 'multiple_days',
        'venues': 'venue_id',
    }, inplace=True)
    df['event_start_date'] = pd.to_datetime(df['event_start_date'])
    df['venue_id'] = df['venue_id'].apply(lambda row: [venue.split('/')[-1].split('?')[0] for venue in row][0])
    df.drop_duplicates(inplace=True)
    # Drop events with the same event_name, venue_id, and event_year
    # Some events have multiple records for every day of the event
    df['event_year'] = df['event_start_date'].dt.year
    df = df.drop_duplicates(subset=['venue_id', 'event_name', 'event_year'], keep='first')
    return df