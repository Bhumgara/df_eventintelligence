from pandas import DataFrame

from apis.venues.client_models.ticketmaster_venues_model import TmVenue
from apis.venues.venue_record import VenueRecord

class TmVenueMapper:
    @staticmethod
    def map_venue_to_record(venue: TmVenue) -> VenueRecord:
        return VenueRecord(
            name=venue.name,
            type=venue.type,
            id=venue.id,
            city=venue.city.name,
            country=venue.country.name,
            postalCode=venue.postalCode,
            longitude=venue.location.longitude,
            latitude=venue.location.latitude
        )

    # @staticmethod
    @staticmethod
    def map_record_to_dict(record: VenueRecord) -> dict:
        return {
            "name": record.name,
            "type": record.type,
            "id": record.id,
            "city": record.city,
            "country": record.country,
            "postalCode": record.postalCode,
            "longitude": record.longitude,
            "latitude": record.latitude
        }


    @staticmethod
    def build_venues_dataframe(venues_json: dict) -> DataFrame:
        venues_models = [
            TmVenueMapper.map_venue_to_record(TmVenue(**venue))
            for venue in venues_json["_embedded"]["venues"]
        ]
        venues_df = DataFrame(
            [TmVenueMapper.map_record_to_dict(vm) for vm in venues_models]
        )
        return venues_df
