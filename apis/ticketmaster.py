import requests
import pandas as pd
import dotenv
import os

dotenv.load_dotenv()

BASE_URL = "https://app.ticketmaster.com/discovery/v2"
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")

def get_nested_value(path, data_dict):
    current = data_dict
    try:
        for key in path:
            current = current[key]
    except:
        current = []
    return current


def get_ticketmaster_data(endpoint, embedded_parts, filters={}) -> pd.DataFrame:
    full_url = f"{BASE_URL}{endpoint}"
    query_params={'apikey': CONSUMER_KEY, 'size': 200}
    query_params.update(filters)

    response = requests.get(full_url, params=query_params)

    print(f"Status Code: {response.status_code}")
    print(f"URL Used: {response.url}")

    flattened_data = {}

    data = response.json()
    for path in embedded_parts:
        flattened_data[path[-1]] = get_nested_value(path, data)

    pages = data["page"]["totalPages"]
    page_no = data["page"]["number"] + 1
    
    for page_no in range(min(pages, 5)):
        next_page={'page': page_no}
        query_params.update(next_page)
        response = requests.get(full_url, params=query_params)
        for path in embedded_parts:
            flattened_data[path[-1]] += get_nested_value(path, response.json())
    return flattened_data
