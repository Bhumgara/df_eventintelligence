import pandas as pd

SUMMER_START_MONTH = 5
SUMMER_END_MONTH = 8


def format_weekend_label(start: pd.Timestamp) -> str:
    if pd.isna(start):
        return ""
    end = start + pd.Timedelta(days=2)
    if start.month == end.month:
        return f"{start.strftime('%b')} {start.day}–{end.day}"
    return f"{start.strftime('%b')} {start.day}–{end.strftime('%b')} {end.day}"


def add_analysis_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["event_start_date"] = pd.to_datetime(df["event_start_date"], errors="coerce")
    df["event_day_name"] = df["event_start_date"].dt.day_name()
    df["event_year"] = df["event_start_date"].dt.year
    df["event_month"] = df["event_start_date"].dt.month
    df["is_summer"] = df["event_month"].between(SUMMER_START_MONTH, SUMMER_END_MONTH)
    df["is_weekend"] = df["event_start_date"].dt.weekday.isin([4, 5, 6])
    df["weekend_start"] = pd.NaT
    mask = df["is_weekend"]
    df.loc[mask, "weekend_start"] = df.loc[mask, "event_start_date"].apply(
        lambda d: d - pd.Timedelta(days=max(0, d.weekday() - 4))
    )
    df["weekend_start"] = pd.to_datetime(df["weekend_start"]).dt.normalize()
    df = df[df["is_summer"]]
    df = df[df["is_weekend"]]
    return df
