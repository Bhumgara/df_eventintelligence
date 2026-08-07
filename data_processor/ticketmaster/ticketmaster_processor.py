

from data_processor.ticketmaster.events_processor import EventsProcessor
from data_processor.ticketmaster.venues_processor import VenuesProcessor


class TicketmasterProcessor:
    def __init__(
            self,
            events_df,
            venues_df,
            events_processor: EventsProcessor, 
            venues_processor: VenuesProcessor
            ):
        self.events_df = events_df
        self.venues_df = venues_df
        self.events_processor = events_processor
        self.venues_processor = venues_processor

    def merge_venues_to_events(self):
        events_df = self.events_processor.clean_events(self.events_df)
        venues_df = self.venues_processor.clean_venues(self.venues_df)
        return events_df.merge(venues_df, how="left", on="venue_id")