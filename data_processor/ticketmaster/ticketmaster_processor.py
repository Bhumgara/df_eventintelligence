from pathlib import Path
import sys

sys.path.insert(0, str(Path.cwd().parent))

import pgeocode as pg
import pandas as pd

import data_processor.ticketmaster.events_processor as ep
import data_processor.ticketmaster.venues_processor as vp

def add_county(df):
    nomi = pg.Nominatim("gb")
    df['venue_county'] = nomi.query_postal_code(df["venue_postal_code"].to_list())["county_name"]
    return df

# def add_regions(df) -> pd.DataFrame:
#     csv_path = Path(__file__).resolve().parents[2] / "assets" / "ons_geographical_regions.csv"
#     df_ons_regions = pd.read_csv(csv_path)
#     df = df.merge(
#         df_ons_regions,
#         how="left",
#         left_on="venue_city",
#         right_on="LAD24NM"
#     )
#     df.rename(columns={"RGN24NM":"venue_region"}, inplace=True)
#     return df

def merge_venues_to_events(events_df, venues_df):
    events_df = ep.clean_events(events_df)
    venues_df = vp.clean_venues(venues_df)
    merged_df = events_df.merge(venues_df, how="left", on="venue_id")
    tckm_df = add_county(merged_df)
    return tckm_df