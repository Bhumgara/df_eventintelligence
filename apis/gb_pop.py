import pgeocode
import pandas as pd
import plotly.express as px

SOURCE = '.\\.data\\pcds_p003.csv'

df_sectors = None
df_districts = None

def load_sector_data() -> pd.DataFrame:
    global df_sectors

    df_sectors = pd.read_csv(SOURCE).rename(
        columns={
            'Postcode Sectors':'sector',
            'Count':'count'
        }
    )
    df_sectors['district'] = df_sectors['sector'].str.split().str[0]

    return df_sectors

def load_district_data() -> pd.DataFrame:
    assert type(df_sectors) == pd.DataFrame, f"Source sector data has not been loaded in. Please run `load_sector_data()` first."

    global df_districts

    districts = df_sectors['district'].unique()
    d2c = get_longlat_for_districts(districts)

    df_sectors_ext = pd.merge(df_sectors, d2c, how='left', left_on='district', right_on='postal_code')

    df_districts = (df_sectors_ext
        .groupby(by=['district','longitude','latitude'], as_index=False)[['count']]
        .sum()
        .rename(columns={'count':'population'})
    )

    return df_districts

def get_longlat_for_districts(districts:str|list[str]) -> pd.Series | pd.DataFrame:
    nomi = pgeocode.Nominatim('gb')
    return nomi.query_postal_code(districts)

def mapplot_districts():
    assert type(df_districts) == pd.DataFrame, f"District data has not been computed yet. Please run `load_district_data()` first."

    # df must contain: district, population, lat, lon
    fig = px.scatter_mapbox(
        df_districts,
        lat="latitude",
        lon="longitude",
        hover_name="district",
        hover_data={"population": True},
        size="population",          # bubble size = population
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

    return fig


if __name__ == '__main__':
    load_sector_data()
    load_district_data()
    mapplot_districts()