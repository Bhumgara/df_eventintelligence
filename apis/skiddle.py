import requests, dotenv, os

# Global variables setup
dotenv.load_dotenv()

BASE_URL = 'https://www.skiddle.com/api/v1/'
API_KEY = os.getenv("SKIDDLE_KEY")



def query(endpoint:str, filters:dict={}, verbose:bool=False) -> dict:
    url = BASE_URL + endpoint
    params = {'api_key': API_KEY}
    params.update(filters)

    if verbose:
        print(f"{url}\n\t{'\n\t'.join(f"{k}: {v}" for k,v in filters.items())}")

    response = requests.get(url, params)

    assert response.status_code == 200, f"Unexpected response code ({response.status_code}): {response.reason}"

    data = response.json()

    return data



def fetch_all_events(filters:dict={}, verbose:bool=False) -> list[dict]:
    endpoint = 'events/search/'
    d_filters = {'limit': 100, 'offset':0}
    d_filters.update(filters)

    collective_results = []

    while d_filters['offset'] < 1000:
        data = query(endpoint, d_filters, verbose=verbose)
        collective_results += data['results']

        if int(data['totalcount']) <= len(collective_results):
            break

        d_filters['offset'] += data['pagecount']

    return collective_results