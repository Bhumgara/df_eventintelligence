import streamlit as st
import pgeocode as pg
import pandas as pd
import plotly.express as px
from utility import api_handler as api
from plotly.graph_objs._figure import Figure
from streamlit_dashboard.Home import update_data


def build_treemap_df(df):
    df_genre_counts = df.groupby(["genre_name", "subgenre_name"]).size().reset_index(name="count")
    return df_genre_counts

def create_genre_treemap(df) -> Figure:
    fig = px.treemap(
        df, 
        path=["genre_name", "subgenre_name"], 
        values="count",
    )
    fig.update_layout(
        coloraxis_showscale=False,
        
        margin=dict(t=50, l=10, r=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    fig.update_traces(
        marker=dict(line=dict(width=1, color="white")),
        
        textinfo="label+value", 
        textposition="middle center",
        textfont=dict(size=16, color="black"),
        insidetextfont=dict(size=14, color="black"),
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percentRoot:.1%}'
    )
    return fig

def create_genre_kpi(df) -> None:
    df_counts = df.groupby(["genre_name", "subgenre_name"]).size().reset_index(name="count")
    
    max_row = df_counts.loc[df_counts["count"].idxmax()]
    max_genre = max_row["genre_name"]
    max_val = max_row["count"]
    
    min_row = df_counts.loc[df_counts["count"].idxmin()]
    min_genre = min_row["genre_name"]
    min_val = min_row["count"]
    
    # Total number of unique subgenres
    total_variety = len(df_counts)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Top Genre", 
            value=max_genre, 
            delta=f"{max_val} events", 
            delta_color="green",
            delta_arrow="off"
        )
        
    with col2:
        st.metric(
            label="Rarest Genre", 
            value=min_genre, 
            delta=f"{min_val} events", 
            delta_color="red",
            delta_arrow="off"
        )
        
    with col3:
        st.metric(
            label="Total Variety", 
            value=total_variety, 
            delta="Unique Genre Combinations",
            delta_color="green",
            delta_arrow="off"
        )

def create_genre_county_heatmap(df) -> Figure:
    heatmap_data = df.groupby(['genre_name', 'venue_county']).size().reset_index(name='count')
    
    pivot = heatmap_data.pivot(index='genre_name', columns='venue_county', values='count').fillna(0)

    fig = px.imshow(
        pivot,
        labels=dict(x="County", y="Genre", color="Frequency"),
        x=pivot.columns,
        y=pivot.index,
        color_continuous_scale="Plasma",
        aspect="auto",
    )

    fig.update_layout(
        xaxis=dict(tickangle=-45, tickfont=dict(size=12)),
        yaxis=dict(tickfont=dict(size=12)),
    )

    fig.update_coloraxes(
        colorbar=dict(
            title="Event Count",
            tickfont=dict(size=12),
        )
    )

    return fig

# def create_genre_region_heatmap(df) -> Figure:
#     df_genre_loc = df[[ "genre_name", "venue_region"]].copy()
#     # df_genre_loc = add_county(df_genre_loc)
#     heatmap_data = df_genre_loc.groupby(['genre_name', 'venue_region']).size().reset_index(name='count')
    
#     pivot = heatmap_data.pivot(index='genre_name', columns='venue_region', values='count').fillna(0)

#     fig = px.imshow(
#         pivot,
#         labels=dict(x="Region", y="Genre", color="Frequency"),
#         x=pivot.columns,
#         y=pivot.index,
#         color_continuous_scale="Plasma",
#         aspect="auto",
#     )

#     fig.update_layout(
#         xaxis=dict(tickangle=-45, tickfont=dict(size=12)),
#         yaxis=dict(tickfont=dict(size=12)),
#     )

#     fig.update_coloraxes(
#         colorbar=dict(
#             title="Event Count",
#             tickfont=dict(size=12),
#         )
#     )

#     return fig


def main():
    df = api.read_ticketmaster_data()
    df = df[df["genre_name"] != "Undefined"]

    logo, left, right = st.columns([2,5,2])
    with logo:
        st.image("eventintelligence-logo.png", width=300)

    with left:
        st.write("# UK Festival Genre Representation")

    with right:
        st.button("Refresh", on_click=update_data, key="GenreRefreshBt")

    st.write("*Are there genre combinations or audience segments that appear underrepresented in the current festival landscape?*")
    st.write('---')
    
    # ----- KPIs ------
    create_genre_kpi(df)

    # ------- Treemap ------------
    df_genres = build_treemap_df(df)

    min_genre_count = int(df_genres["count"].min())
    max_genre_count = int(df_genres["count"].max())
    
    st.write("## Distribution of Festival Genres and Subgenres")
    count_threshold = st.slider(
        "Minimum occurrences to show:", 
        min_value=min_genre_count, 
        max_value=max_genre_count, 
        value=max_genre_count
    )
    
    df_filtered = df_genres[df_genres["count"] <= count_threshold]
    fig_genre_treemap = create_genre_treemap(df_filtered)
    st.plotly_chart(fig_genre_treemap)

    st.write("---")

    # ------ Heatmap ----
    st.write("## Heatmap: Event Genre vs County")
    st.plotly_chart(create_genre_county_heatmap(df))


if __name__ == "__main__":
    main()