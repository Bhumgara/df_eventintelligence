

from pandas import DataFrame
from pydantic import ValidationError

from apis.venues.client_models.ticketmaster_venues_model import TmVenue
from apis.venues.venue_record import VenueRecord
from apis.venues.venues_mapper import TmVenueMapper


class VenuesProcessor:
    def __init__(self):
        pass
       
    @staticmethod
    def build_venues_dataframe(venues: list[VenueRecord]) -> DataFrame:
        venues_df = DataFrame(
            [TmVenueMapper.map_record_to_dict(vm) for vm in venues]
        )
        return venues_df

    @staticmethod
    def validate_venues(venues_response):
        valid_venues = []
        invalid_venues = []

        for venue in venues_response:
            try:
                valid_venues.append(TmVenueMapper.map_venue_to_record(TmVenue(**venue)))
            except ValidationError as e:
                invalid_venues.append({"venue": venue, "error": str(e)})

        print(f"Valid venues: {len(valid_venues)}, Invalid venues: {len(invalid_venues)}")

        if len(valid_venues) == 0:
            raise Exception('No venues match schema.')

        return valid_venues, invalid_venues

    @staticmethod
    def clean_venues(df: DataFrame) -> DataFrame:
        df.rename(columns={
            'id': 'venue_id',
            'name': 'venue_name',
            'type': 'venue_type',
            'city': 'venue_city',
            'country': 'venue_country',
            'postalCode': 'venue_postal_code',
            'longitude': 'venue_longitude',
            'latitude': 'venue_latitude',
        }, inplace=True)

        df.drop_duplicates(inplace=True)

        return df