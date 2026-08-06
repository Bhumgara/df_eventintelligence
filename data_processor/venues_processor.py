

from pandas import DataFrame
from pydantic import ValidationError

from apis.venues.client_models.venues_model import Venue
from apis.venues.venue_record import VenueRecord
from apis.venues.venues_mapper import VenueMapper


class VenuesProcessor:
       
    @staticmethod
    def build_venues_dataframe(venues: list[VenueRecord]) -> DataFrame:
        venues_df = DataFrame(
            [VenueMapper.map_record_to_dict(vm) for vm in venues]
        )
        return venues_df

    @staticmethod
    def validate_venues(venues_response):
        valid_venues = []
        invalid_venues = []

        for venue in venues_response:
            print(venue)
            try:
                valid_venues.append(VenueMapper.map_venue_to_record(Venue(**venue)))
            except ValidationError as e:
                print(e)
                invalid_venues.append({"venue": venue, "error": str(e)})

        print(f"Valid venues: {len(valid_venues)}, Invalid venues: {len(invalid_venues)}")

        if len(valid_venues) == 0:
            raise Exception('No venues match schema.')

        return valid_venues, invalid_venues
        