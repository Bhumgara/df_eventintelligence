
from apis.venues.client_models.venues_model import Venue
from apis.venues.venue_record import VenueRecord
from pandas import DataFrame

class VenueMapper:
    @staticmethod
    def map_venue_to_record(venue: Venue) -> VenueRecord:
        return VenueRecord(
            name=venue.name,
            type=venue.type,
            id=venue.id,
            city=venue.city.name,
            country=venue.country.name,
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
            "longitude": record.longitude,
            "latitude": record.latitude
        }


    @staticmethod
    def build_venues_dataframe(venues_json: dict) -> DataFrame:
        venues_models = [
            VenueMapper.map_venue_to_record(Venue(**venue))
            for venue in venues_json["_embedded"]["venues"]
        ]
        venues_df = DataFrame(
            [VenueMapper.map_record_to_dict(vm) for vm in venues_models]
        )
        return venues_df