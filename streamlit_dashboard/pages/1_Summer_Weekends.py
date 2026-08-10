'''
Which weekends in the summer window are already heavily loaded with competing events, and which are relatively clear?
'''
import sys
print(sys.path[0])

from streamlit_dashboard.Home import update_data

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_dashboard.utility import api_handler as api
from streamlit_dashboard.utility.analysis import SUMMER_START_MONTH, SUMMER_END_MONTH, add_analysis_columns, format_weekend_label
from plotly.graph_objs._figure import Figure
from streamlit_dashboard.utility.styles import PRIMARY, SECONDARY, ACCENT, DARK, LIGHT, NEUTRAL


BINS = [-1, 0, 5, 15, float("inf")]
FULLNESS_LABELS = ["Gap (0)", "Light (1–5)", "Moderate (6–15)", "Heavy (16+)"]
FULLNESS_COLORS = {
    "Gap (0)":         PRIMARY,
    "Light (1–5)":     SECONDARY,
    "Moderate (6–15)": ACCENT,
    "Heavy (16+)":     DARK,
}

def streamlit_header(df):
    st.session_state.setdefault('data', pd.DataFrame())

    logo, left, right = st.columns([3,5,1])
    with logo:
        st.image("eventintelligence-logo.png", width=300)

    with left:
        st.header("Gaps in the UK live music calendar")

    with right:
        st.button("Refresh", on_click=update_data(), key="SummerRefreshBtn")

    df = add_analysis_columns(df)
    years = sorted(df["event_year"].dropna().unique().tolist())
    if not years:
        st.error("No valid event years were found in the dataset.")

    selected_year = st.selectbox("Year", years, index=len(years) - 1)

    df = df[df["event_year"] == selected_year]

    if df.empty:
        st.warning("No summer data is available for the selected year.")

    total_events = len(df)
    unique_counties = df["venue_county"].nunique(dropna=True)
    weekend_count = df["weekend_start"].nunique(dropna=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Summer listings", total_events)
    col2.metric("Distinct counties", unique_counties)
    col3.metric("Weekends with events", weekend_count)
    return selected_year, df

def build_weekend_data(df: pd.DataFrame, year: int) -> pd.DataFrame:
    weekend_start = pd.Timestamp(year, SUMMER_START_MONTH, 1)
    weekend_end = pd.Timestamp(year, SUMMER_END_MONTH, 31)
    first_friday = weekend_start + pd.Timedelta(days=(4 - weekend_start.weekday()) % 7)
    all_fridays = pd.date_range(start=first_friday, end=weekend_end, freq="7D")

    df_ex = pd.DataFrame({
        "weekend_start": all_fridays,
        "weekend_label": [format_weekend_label(f) for f in all_fridays],
    })

    event_counts = (
        df[df["weekend_start"].notna()]
        .groupby("weekend_start", dropna=True)
        .size()
        .reset_index(name="event_count")
    )

    df_ex = df_ex.merge(event_counts, on="weekend_start", how="left")
    df_ex["event_count"] = df_ex["event_count"].fillna(0).astype(int)
    df_ex["fullness"] = pd.cut(df_ex["event_count"], bins=BINS, labels=FULLNESS_LABELS).astype(str)
    return df_ex.sort_values("weekend_start").reset_index(drop=True)


def create_weekend_bar(df: pd.DataFrame) -> Figure:
    df_plot = df.iloc[::-1].reset_index(drop=True)
    fig = px.bar(
        df_plot,
        x="event_count",
        y="weekend_label",
        orientation="h",
        color="fullness",
        color_discrete_map=FULLNESS_COLORS,
        labels={"event_count": "Festival listings", "weekend_label": "Weekend", "fullness": "Fullness"},
    )
    fig.update_yaxes(categoryorder="array", categoryarray=df_plot["weekend_label"].tolist()) # Sourced from Gemini
    fig.update_layout(legend_title_text="Fullness")
    return fig


def show_gap_callout(df: pd.DataFrame) -> None:
    low_event_count = df[df["event_count"] <= 2].sort_values("event_count")
    if low_event_count.empty:
        st.info("No weekends with 2 or fewer festival listings were found in this summer.")
        return
    st.success(
        f"**{len(low_event_count)} potentially clear weekend(s)** show 2 or fewer Ticketmaster listings — "
        "the strongest gap candidates from this dataset."
    )
    st.dataframe(
        low_event_count[["weekend_label", "event_count", "fullness"]].rename(columns={
            "weekend_label": "Weekend", "event_count": "Festival listings", "fullness": "Fullness"
        }), width='stretch'
    )

def main():
    st.write("# 📅 Summer Weekend Fullness")

    df = api.read_ticketmaster_data()
    if df is None or df.empty:
        st.error("No Ticketmaster data is available. Run the local ingestion script or refresh the data source.")

    selected_year, df = streamlit_header(df)

    st.write("---")
    st.write("## Weekend fullness across the summer.")
    st.caption("Green = potential gap; red = heavily occupied. All weekends shown, including zero-listing weeks.")
    df_ex = build_weekend_data(df, int(selected_year))
    st.plotly_chart(create_weekend_bar(df_ex), width='stretch')

    st.write("---")
    st.write("## Gap candidates: quietest weekends")
    show_gap_callout(df_ex)

if __name__ == "__main__":
    main()
