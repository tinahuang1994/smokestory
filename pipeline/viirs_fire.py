import io
import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

MAP_KEY = os.getenv("FIRMS_MAP_KEY")


def get_active_fires(bbox, day_range):
    url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/VIIRS_SNPP_NRT/{bbox}/{day_range}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_csv(io.StringIO(response.text))
        return df
    except requests.RequestException as e:
        print(f"Error fetching FIRMS fire data: {e}")
        return None


if __name__ == "__main__":
    df = get_active_fires("-124.4,32.5,-114.1,42.0", 1)
    if df is not None:
        print(df.shape)
        print(df.head(3))
