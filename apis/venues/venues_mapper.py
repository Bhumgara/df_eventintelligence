
from pydantic import ValidationError

from apis.venues.client_models.venues_model import Venue
from apis.venues.venue_record import VenueRecord

class VenueMapper:
    @staticmethod
    def map_venue_to_record(venue: Venue) -> VenueRecord:
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