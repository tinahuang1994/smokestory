import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

GUARDIAN_API_KEY = os.getenv("GUARDIAN_API_KEY", "test")


def get_news_headlines(county_name, date):
    # Use a ±1 day window: major fire stories are often filed the day after ignition
    event_date = datetime.strptime(date, "%Y%m%d")
    from_date = (event_date - timedelta(days=1)).strftime("%Y-%m-%d")
    to_date = (event_date + timedelta(days=1)).strftime("%Y-%m-%d")
    params = {
        "q": f"{county_name} wildfire smoke California",
        "from-date": from_date,
        "to-date": to_date,
        "order-by": "relevance",
        "page-size": 5,
        "api-key": GUARDIAN_API_KEY,
        "show-fields": "headline,trailText",
    }
    try:
        response = requests.get("https://content.guardianapis.com/search", params=params)
        response.raise_for_status()
        results = response.json().get("response", {}).get("results", [])
        # Filter to wildfire/smoke/air quality articles only — prevents unrelated
        # news (crime, politics, sports) from bleeding into narratives
        RELEVANT_KEYWORDS = {
            "fire", "fires", "wildfire", "wildfires", "smoke", "blaze", "blazes",
            "evacuation", "evacuate", "air quality", "pm2.5", "particulate",
            "burn", "burning", "inferno", "firefighter",
        }
        filtered = []
        for r in results:
            text = (
                (r.get("fields", {}).get("headline") or r.get("webTitle") or "") +
                " " +
                (r.get("fields", {}).get("trailText") or "")
            ).lower()
            if any(kw in text for kw in RELEVANT_KEYWORDS):
                filtered.append(r)
        return [
            {
                "title": r.get("fields", {}).get("headline") or r.get("webTitle"),
                "summary": r.get("fields", {}).get("trailText", ""),
                "source": "The Guardian",
                "url": r.get("webUrl"),
            }
            for r in filtered
        ]
    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        return []


if __name__ == "__main__":
    headlines = get_news_headlines("Los Angeles", "20250109")
    for h in headlines:
        print(h)
