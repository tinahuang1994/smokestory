import os
import requests
from dotenv import load_dotenv

load_dotenv()

GUARDIAN_API_KEY = os.getenv("GUARDIAN_API_KEY", "test")


def get_news_headlines(county_name, date):
    formatted_date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
    params = {
        "q": f"{county_name} wildfire smoke California",
        "from-date": formatted_date,
        "to-date": formatted_date,
        "order-by": "relevance",
        "page-size": 3,
        "api-key": GUARDIAN_API_KEY,
        "show-fields": "headline,trailText",
    }
    try:
        response = requests.get("https://content.guardianapis.com/search", params=params)
        response.raise_for_status()
        results = response.json().get("response", {}).get("results", [])
        return [
            {
                "title": r.get("fields", {}).get("headline") or r.get("webTitle"),
                "source": "The Guardian",
                "url": r.get("webUrl"),
            }
            for r in results
        ]
    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        return []


if __name__ == "__main__":
    headlines = get_news_headlines("Los Angeles", "20250109")
    for h in headlines:
        print(h)
