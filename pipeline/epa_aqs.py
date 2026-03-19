import os
import requests
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EPA_AQS_EMAIL")
KEY = os.getenv("EPA_AQS_KEY")


def get_pm25_readings(state_code, start_date, end_date):
    url = "https://aqs.epa.gov/data/api/dailyData/byState"
    params = {
        "email": EMAIL,
        "key": KEY,
        "param": "88101",
        "bdate": start_date,
        "edate": end_date,
        "state": state_code,
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("Data", [])
    except requests.RequestException as e:
        print(f"Error fetching PM2.5 data: {e}")
        return []


if __name__ == "__main__":
    readings = get_pm25_readings("06", "20240101", "20240107")
    for r in readings[:3]:
        print(r)
