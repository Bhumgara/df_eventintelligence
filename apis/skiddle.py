import requests, dotenv, os, pandas as pd
from pydantic import ValidationError

import events.events_mapper as EMapper
import events.event_record as ERecord
import events.client_models.skiddle_event_model as skem

# Global variables setup
dotenv.load_dotenv()

BASE_URL = 'https://www.skiddle.com/api/v1/'
API_KEY = os.getenv("SKIDDLE_KEY")



def query(endpoint:str, filters:dict={}, verbose:bool=False) -> dict:
    url = BASE_URL + endpoint
    params = {'api_key': API_KEY}
    params.update(filters)

    if verbose:
        print(f"{url}\n\t{'\n\t'.join(f"{k}: {v}" for k,v in filters.items())}")

    response = requests.get(url, params)

    assert response.status_code == 200, f"Unexpected response code ({response.status_code}): {response.reason}"

    data = response.json()

    return data



def fetch_all_events(filters:dict={}, verbose:bool=False) -> list[dict]:
    endpoint = 'events/search/'
    d_filters = {'limit': 100, 'offset':0}
    d_filters.update(filters)

    collective_results = []

    while d_filters['offset'] < 1000:
        data = query(endpoint, d_filters, verbose=verbose)
        collective_results += data['results']

        if int(data['totalcount']) <= len(collective_results):
            break

        d_filters['offset'] += data['pagecount']

    return collective_results

def validate_events(events:list[dict], return_invalid:bool=False) -> list[ERecord.EventRecord]:
    # Validate each event has been fetched in the expected format
    event_models = []
    invalid_events = []
    for e in events:
        try:
            event_models.append(skem.Event(**e))
        except ValidationError as e:
            print(e)
            invalid_events.append(e)

    # Map validated events to a consistent record format
    event_records = [EMapper.SkEventMapper.map_event_to_record(e) for e in event_models]

    # Return invalid events if requested
    if return_invalid: return event_records, invalid_events
    else: return event_records

def events_to_df(events:list[dict]|list[ERecord.EventRecord], keys:list[str]=None):
    # Convert EventRecords to dict if not already done so
    if type(events) != dict:
        events = [EMapper.TmEventMapper.map_event_record_to_dict(e) for e in events]
    return pd.DataFrame(events)