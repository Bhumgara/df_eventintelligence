from apis import ticketmaster as tck
from data_processor.ticketmaster.venues_processor import VenuesProcessor
from data_processor.ticketmaster.ticketmaster_processor import TicketmasterProcessor
from data_processor.ticketmaster.events_processor import EventsProcessor
import json
import os

TICKETMASTER_EVENTS_DATA = "tck_events.json"
TICKETMASTER_VENUES_DATA = "tck_veneus.json"
API_DATA_FOLDER = ".api_data"

def read_local_api_data(filename):
    with open(f"{API_DATA_FOLDER}/{filename}", 'r') as file:
        data = json.load(file)
    return data

def write_api_to_json(filename: str, response):
    if not os.path.exists(API_DATA_FOLDER):
        os.mkdir(API_DATA_FOLDER)
    with open(f"{API_DATA_FOLDER}/{filename}", "w") as file:
        json.dump(response, file, indent=4)

def call_ticketmaster_api():
    endpoint = "/venues.json"
    embedded_parts = [("_embedded", "venues")]
    kword_filters_gb= {"countryCode":"GB"}
    kword_filters_uk= {"countryCode":"UK"}
    venues_list = []

    response_data_gb = tck.get_ticketmaster_data(endpoint, embedded_parts, filters=kword_filters_gb)
    response_data_uk = tck.get_ticketmaster_data(endpoint, embedded_parts, filters=kword_filters_uk)
    venues_list = response_data_gb + response_data_uk

    endpoint = "/events.json"
    embedded_parts = [("_embedded", "events")]
    kword_filters_gb= {"classificationName":"festival", "countryCode":"GB"}
    kword_filters_uk= {"classificationName":"festival", "countryCode":"UK"}
    events_list = []

    response_data_gb = tck.get_ticketmaster_data(endpoint, embedded_parts, filters=kword_filters_gb)
    response_data_uk = tck.get_ticketmaster_data(endpoint, embedded_parts, filters=kword_filters_uk)
    events_list = response_data_gb + response_data_uk

    write_api_to_json(TICKETMASTER_EVENTS_DATA, events_list)
    write_api_to_json(TICKETMASTER_VENUES_DATA, venues_list)
    print("Local Ticketmaster API successfully updated.")


def read_ticketmaster_data():

    try:
        events_list = read_local_api_data(TICKETMASTER_EVENTS_DATA)
        venues_list = read_local_api_data(TICKETMASTER_VENUES_DATA)
    except OSError as e:
        print("Failed to read local Ticketmaster data, recalling API.")
        call_ticketmaster_api()
        try:
            events_list = read_local_api_data(TICKETMASTER_EVENTS_DATA)
            venues_list = read_local_api_data(TICKETMASTER_VENUES_DATA)
        except OSError as e:
            print("Failed to retrieve Ticketmaster API data.")
            return

    
    venues_models, invalid_models = VenuesProcessor.validate_venues(venues_list)
    venues_df = VenuesProcessor.build_venues_dataframe(venues_models)

    events_models, invalid_events_models = EventsProcessor.validate_events(events_list)
    events_df = EventsProcessor.build_events_dataframe(events_models)

    vn_copy = venues_df.copy()
    ev_copy = events_df.copy()

    evp = EventsProcessor()
    vnp = VenuesProcessor()


    tmp = TicketmasterProcessor(ev_copy, vn_copy, evp, vnp)
    merged_df = tmp.merge_venues_to_events()

    return(merged_df)

def update_session_data():
    call_ticketmaster_api()
    return read_ticketmaster_data()