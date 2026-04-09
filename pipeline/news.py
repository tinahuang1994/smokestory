import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

GUARDIAN_API_KEY = os.getenv("GUARDIAN_API_KEY", "test")


RELEVANT_KEYWORDS = {
    "fire", "fires", "wildfire", "wildfires", "smoke", "blaze", "blazes",
    "evacuation", "evacuate", "air quality", "pm2.5", "particulate",
    "burn", "burning", "inferno", "firefighter",
}


def _filter_relevant(results):
    """Keep only wildfire/smoke/air quality articles."""
    filtered = []
    for r in results:
        text = (
            (r.get("fields", {}).get("headline") or r.get("webTitle") or "") +
            " " +
            (r.get("fields", {}).get("trailText") or "")
        ).lower()
        if any(kw in text for kw in RELEVANT_KEYWORDS):
            filtered.append(r)
    return filtered


def _format_results(results):
    return [
        {
            "title": r.get("fields", {}).get("headline") or r.get("webTitle"),
            "summary": r.get("fields", {}).get("trailText", ""),
            "source": "The Guardian",
            "url": r.get("webUrl"),
        }
        for r in results
    ]


def _query_guardian(q, from_date, to_date, page_size=5):
    params = {
        "q": q,
        "from-date": from_date,
        "to-date": to_date,
        "order-by": "relevance",
        "page-size": page_size,
        "api-key": GUARDIAN_API_KEY,
        "show-fields": "headline,trailText",
    }
    response = requests.get("https://content.guardianapis.com/search", params=params)
    response.raise_for_status()
    return response.json().get("response", {}).get("results", [])


def get_news_headlines(county_name, date):
    # Use a ±1 day window: major fire stories are often filed the day after ignition
    event_date = datetime.strptime(date, "%Y%m%d")
    from_date = (event_date - timedelta(days=1)).strftime("%Y-%m-%d")
    to_date = (event_date + timedelta(days=1)).strftime("%Y-%m-%d")

    try:
        # Primary query: county-specific
        results = _query_guardian(
            f"{county_name} wildfire smoke California", from_date, to_date
        )
        filtered = _filter_relevant(results)

        # Fallback: if county query returns nothing, try broader CA wildfire query.
        # This catches major named fires (e.g. Camp Fire, Carr Fire) where Guardian
        # headlined the fire name rather than the county name.
        if not filtered:
            results = _query_guardian(
                "California wildfire smoke fire", from_date, to_date, page_size=8
            )
            filtered = _filter_relevant(results)

        return _format_results(filtered)
    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        return []


if __name__ == "__main__":
    headlines = get_news_headlines("Los Angeles", "20250109")
    for h in headlines:
        print(h)
