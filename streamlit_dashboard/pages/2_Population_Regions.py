'''
Are there UK regions where live music event density is low relative to their size or population?
'''

import streamlit as st
import plotly.express as px
import pandas as pd
import pgeocode as pg
import re

from utility import api_handler as api

from pathlib import Path
import sys

sys.path.insert(0, str(Path.cwd().parent))
print('='*20+'>', Path.cwd().parent)
import apis.census as cs



def plot_district_populations(districts:pd.DataFrame, plot_to_sl:bool=True):

    fig = px.scatter_map(
        districts,
        lat="latitude",
        lon="longitude",
        hover_name="district",
        hover_data={"population": True},
        size="population",
        size_max=12,
        color="population",
        color_continuous_scale="Viridis",
        zoom=5.5,
        height=650,
        opacity=0.5
    )

    fig.update_layout(
        mapbox_style="carto-positron",
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    if plot_to_sl:
        st.write(fig)

    return fig



def get_district_event_density(events:pd.DataFrame):
    districts = []
    for i,e in events['venue_postal_code'].items():
        if type(e) != str:
            districts.append(pd.NA)
            continue
        search = re.search('([A-Z]+)([0-9]+).*?[A-Z0-9]{3}', e.replace(' ',''))
        districts.append(search.group(1)+search.group(2))


    events['venue_postal_district'] = districts
    event_density = (events
        .groupby(by=['venue_postal_district','venue_county'])
        .size()
        .to_frame('count')
        .reset_index()
    )
    event_density[['longitude', 'latitude']] = (pg.Nominatim('gb')
        .query_postal_code(event_density['venue_postal_district'].values)
        [['longitude','latitude']]
    )

    return event_density

def plot_district_event_desity(event_density:pd.DataFrame, plot_to_sl:bool=True):

    fig = px.scatter_map(
        event_density,
        lat="latitude",
        lon="longitude",
        hover_name="venue_postal_district",
        hover_data={"venue_county":True, "count": True},
        size="count",
        size_max=20,
        color="count",
        color_continuous_scale="Viridis",
        zoom=5.5,
        height=650,
        opacity=0.5
    )

    fig.update_layout(
        mapbox_style="carto-positron",
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    if plot_to_sl:
        st.write(fig)

    return fig



def main():
    # ----- Set page config -----
    st.set_page_config(layout='wide')

    # ----- Page title & headers -----
    st.write('# UK Population to Festival Density')
    st.write('*Are there UK regions where live music event density is low relative to their size or population?*')
    st.write('---')

    col1, col2 = st.columns(2)

    with col1:
        st.write('### UK Population by District')
        df_sectors = cs.load_sector_data()
        df_districts = cs.load_district_data(df_sectors)

        # Plot stats
        df_counties = (df_districts
            .groupby(by='county_name')['population']
            .sum()
            .reset_index()
            .sort_values('population', ascending=False)
        )
        counties = zip(df_counties.iloc[:3].values, st.columns(3))
        for i, (county,col) in enumerate(counties):
            with col:
                st.metric(
                    label=f'#{i+1} Highest Populated County',
                    value=county[0].replace('Greater', ''),
                    delta=f"{county[1]:,} population"
                )

        # Plot map
        plot_district_populations(df_districts)

    with col2:
        st.write('### UK Festival Density by District')
        df_tk = api.read_ticketmaster_data()
        df_event_density = get_district_event_density(df_tk).sort_values(by='count', ascending=False)

        # Plot stats
        counties = zip(df_event_density.iloc[:3].values, st.columns(3))
        for i, (county,col) in enumerate(counties):
            with col:
                st.metric(
                    label=f'#{i+1} Highest Fest. Density County',
                    value=county[1],
                    delta=f"{county[2]} festivals"
                )

        # Plot map
        plot_district_event_desity(df_event_density)


if __name__ == '__main__':
    main()