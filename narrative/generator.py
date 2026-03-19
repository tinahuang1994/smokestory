import os
import anthropic
from datetime import datetime
from dotenv import load_dotenv

from pipeline.news import get_news_headlines

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def generate_narrative(county_data, date=None):
    county_name = county_data.get("county_name", "Unknown County")
    pm25_mean = county_data.get("pm25_mean")
    smoke_density = county_data.get("smoke_density")
    has_smoke = county_data.get("has_smoke", False)

    if has_smoke and smoke_density:
        smoke_info = f"Smoke is present with {smoke_density.lower()} density."
    else:
        smoke_info = "No smoke is currently detected in this area."

    if pm25_mean is not None:
        pm25_info = f"{pm25_mean:.2f} µg/m³ (daily average from EPA ground monitors)"
    else:
        pm25_info = "No ground-based PM2.5 monitor data available"

    if date:
        try:
            formatted_date = datetime.strptime(date, "%Y%m%d").strftime("%B %-d, %Y")
        except ValueError:
            formatted_date = date
    else:
        formatted_date = "Unknown date"

    news_section = ""
    if date:
        headlines = get_news_headlines(county_name, date)
        if headlines:
            lines = "\n".join(
                f"- \"{h['title']}\" ({h['source']})" for h in headlines
            )
            news_section = f"Relevant news headlines from this date:\n{lines}\n"

    prompt = f"""You are writing a compelling narrative for SmokeStory — an AI-powered wildfire smoke tool for California journalists and communities.

Location: {county_name} County, California
Date: {formatted_date}
PM2.5 level: {pm25_info}
Smoke: {smoke_info}

{news_section}
Write a 4-sentence narrative that:
- Opens with the human story or event causing the smoke (use news context if available)
- Connects the event to the specific air quality data
- Gives clear health guidance appropriate to the PM2.5 level
- Ends with one sentence of broader context or what this means for the community

Tone: Journalistic but accessible. Factual but human.
Do NOT start with "On [date]". Do NOT use bullet points.
Write flowing prose that reads like a news story opening paragraph."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


if __name__ == "__main__":
    result = generate_narrative({
        "county_name": "Los Angeles",
        "state": "06",
        "pm25_mean": 44.85,
        "smoke_density": "Light",
        "has_smoke": True,
    }, date="20250109")
    print(result)
