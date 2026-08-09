import dotenv, os
import pgeocode
import pandas as pd
import plotly.express as px

dotenv.load_dotenv()
DATA_SOURCE = os.getenv('SOURCE_CENSUS_DATA')

def load_sector_data() -> pd.DataFrame:

    df_sectors = pd.read_csv(DATA_SOURCE).rename(
        columns={
            'Postcode Sectors':'sector',
            'Count':'count'
        }
    )
    df_sectors['district'] = df_sectors['sector'].str.split().str[0]

    return df_sectors

def load_district_data(sectors:dict|pd.DataFrame) -> pd.DataFrame:
    districts = sectors['district'].unique()

    d2c = get_longlat_for_districts(districts)

    df_sectors_ext = pd.merge(sectors, d2c, how='left', left_on='district', right_on='postal_code')

    df_districts = (df_sectors_ext
        .groupby(by=['district','longitude','latitude'], as_index=False)[['count']]
        .sum()
        .rename(columns={'count':'population'})
    )

    return df_districts

def get_longlat_for_districts(districts:str|list[str]) -> pd.Series | pd.DataFrame:
    nomi = pgeocode.Nominatim('gb')
    return nomi.query_postal_code(districts)

def mapplot_districts(districts:pd.DataFrame):

    fig = px.scatter_mapbox(
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

    return fig


if __name__ == '__main__':
    load_sector_data()
    load_district_data()
    mapplot_districts()