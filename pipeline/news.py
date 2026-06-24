import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

GUARDIAN_API_KEY = os.getenv("GUARDIAN_API_KEY", "test")


RELEVANT_KEYWORDS = {
    # Unambiguous wildfire/smoke terms only — "fire", "fires", "burn", "burning"
    # are excluded because they match common English idioms
    # ("under fire", "fire and rehire", "burning question") producing junk articles
    "wildfire", "wildfires", "smoke", "blaze", "blazes",
    "evacuation", "evacuate", "air quality", "pm2.5", "particulate",
    "inferno", "firefighter", "firefighters",
}


# California-location signals. The broad fallback query ("California wildfire
# smoke") is ranked by Guardian relevance and can surface wildfire articles about
# the UK, Australia, Greece, etc. Those must never reach the narrative (the S4
# rule forbids out-of-state/out-of-country events), so fallback results are
# additionally required to mention California.
CALIFORNIA_SIGNALS = {
    "california", "californ", "calif.", " ca ", "los angeles", "san francisco",
    "san diego", "sacramento", "sonoma", "napa", "yosemite", "sierra nevada",
    "bay area", "southern california", "northern california",
}


def _mentions_california(text):
    return any(sig in text for sig in CALIFORNIA_SIGNALS)


def _article_text(r):
    return (
        (r.get("fields", {}).get("headline") or r.get("webTitle") or "")
        + " "
        + (r.get("fields", {}).get("trailText") or "")
    ).lower()


def _filter_relevant(results, require_california=False):
    """Keep only wildfire/smoke/air quality articles.

    When require_california is True (used for the broad fallback query), also
    require an explicit California signal so non-California wildfire coverage is
    dropped before it can reach the narrative prompt.
    """
    filtered = []
    for r in results:
        text = _article_text(r)
        if not any(kw in text for kw in RELEVANT_KEYWORDS):
            continue
        if require_california and not _mentions_california(text):
            continue
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

        # Fallback: if county query returns nothing, try broader CA wildfire query
        # with a wider ±3 day window. Major named fires (e.g. Camp Fire, Carr Fire)
        # are often headlined without the county name, and Guardian coverage can
        # appear 2–3 days after ignition.
        if not filtered:
            fallback_from = (event_date - timedelta(days=3)).strftime("%Y-%m-%d")
            fallback_to = (event_date + timedelta(days=3)).strftime("%Y-%m-%d")
            results = _query_guardian(
                "California wildfire smoke", fallback_from, fallback_to, page_size=8
            )
            filtered = _filter_relevant(results, require_california=True)

        return _format_results(filtered)
    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        return []


if __name__ == "__main__":
    headlines = get_news_headlines("Los Angeles", "20250109")
    for h in headlines:
        print(h)
