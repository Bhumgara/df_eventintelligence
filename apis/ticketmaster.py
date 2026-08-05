import requests
import pandas as pd
import dotenv
import os

dotenv.load_dotenv()

BASE_URL = "https://app.ticketmaster.com/discovery/v2"
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")

def get_ticketmaster_data(endpoint, filters={}) -> pd.DataFrame:
    full_url = f"{BASE_URL}{endpoint}"
    query_params={'apikey': CONSUMER_KEY}
    query_params.update(filters)

    response = requests.get(full_url, params=query_params)

    print(f"Status Code: {response.status_code}")
    print(f"URL Used: {response.url}")

    data = response.json()

    return data
