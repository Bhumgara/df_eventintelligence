
import pandas as pd


def build_skiddle_tckm_df(tckm_df, skiddle_df) -> pd.DataFrame:

    df_skiddle_small = skiddle_df[["name", "startdate", "enddate", "postcode", "longitude", "latitude"]]
    df_tckm_small = tckm_df[["event_name", "event_start_date", "venue_postal_code", "venue_longitude", "venue_latitude"]]

    # Ensure data from both apis are in consistent format
    df_skiddle_small['enddate'] = pd.to_datetime(df_skiddle_small['enddate'])
    df_skiddle_small['startdate'] = pd.to_datetime(df_skiddle_small['startdate'])
    df_tckm_small["event_start_date"] = pd.to_datetime(df_tckm_small["event_start_date"], utc=True)
    df_skiddle_small.rename(columns={
        "name": "event_name",
        "startdate": "event_start_date",
        "enddate": "event_end_date",
        "postcode": "venue_postal_code",
        "longitude": "venue_longitude",
        "latitude": "venue_latitude"
    }, inplace=True)

    # Merge tickmaster and skiddle rows and remove duplicate events
    df_small_merged = pd.concat([df_skiddle_small, df_tckm_small], ignore_index=True)
    df_small_merged = df_small_merged.drop_duplicates(subset=["event_name"])

    return df_small_merged