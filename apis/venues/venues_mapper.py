from pandas import DataFrame

from apis.venues.client_models.ticketmaster_venues_model import TmVenue
from apis.venues.client_models.skiddle_venues_model import SkVenue
from apis.venues.venue_record import TmVenueRecord, SkVenueRecord

class TmVenueMapper:
    @staticmethod
    def map_venue_to_record(venue: TmVenue) -> TmVenueRecord:
        return TmVenueRecord(
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
    def map_record_to_dict(record: TmVenueRecord) -> dict:
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

class SkVenueMapper:
    @staticmethod
    def map_venue_record_to_dict(record: SkVenueRecord) -> dict:
        # return {
        #     "id": record.id,
        #     "name": record.name,
        #     "type": record.type,
        #     "town": record.town,
        #     "postcode": record.postcode,
        #     "longitude": record.longitude,
        #     "latitude": record.latitude,
        # }
        return record.model_dump()
    
    @staticmethod
    def map_venue_to_record(venue: SkVenue) -> SkVenueRecord:
        return SkVenueRecord(
             id = venue.id,
             name = venue.name,
             type = venue.type,
             town = venue.town,
             postcode = venue.postcode,
             longitude = venue.longitude,
             latitude = venue.latitude
        )