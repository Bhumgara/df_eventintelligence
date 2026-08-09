from pathlib import Path
import sys

sys.path.insert(0, str(Path.cwd().parent))
print(Path.cwd().parent)

from apis import ticketmaster as tck
from data_processor.ticketmaster.venues_processor import VenuesProcessor
from data_processor.ticketmaster.ticketmaster_processor import TicketmasterProcessor
from data_processor.ticketmaster.events_processor import EventsProcessor

def call_api():
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