import os
import anthropic
from datetime import datetime
from dotenv import load_dotenv

from pipeline.news import get_news_headlines

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def get_severity_label(pm25):
    if pm25 is None:
        return None
    if pm25 <= 9.0:
        return "Good"
    elif pm25 <= 35.4:
        return "Moderate"
    elif pm25 <= 55.4:
        return "Unhealthy for Sensitive Groups"
    elif pm25 <= 150.4:
        return "Unhealthy"
    elif pm25 <= 250.4:
        return "Very Unhealthy"
    else:
        return "Hazardous"


def generate_narrative(county_data, date=None):
    county_name = county_data.get("county_name", "Unknown County")
    pm25_mean = county_data.get("pm25_mean")
    smoke_density = county_data.get("smoke_density")
    has_smoke = county_data.get("has_smoke") or False

    severity = get_severity_label(pm25_mean)

    if has_smoke and smoke_density:
        smoke_info = f"Smoke is present with {str(smoke_density).lower()} density."
    else:
        smoke_info = "No smoke is currently detected in this area."

    if pm25_mean is not None:
        pm25_info = f"{pm25_mean:.2f} µg/m³ — classified as {severity} by EPA standards"
    else:
        pm25_info = "No ground-based PM2.5 monitor data available"

    if date:
        try:
            formatted_date = (
                datetime.strptime(date, "%Y%m%d")
                .strftime("%B %d, %Y")
                .replace(" 0", " ")
            )
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
            news_section = f"Relevant news headlines from this date:\n{lines}"

    # ── Build prompt sections ──────────────────────────────────
    opening_instruction = (
        "If smoke or fire is present, open with the human story behind it. "
        "If no smoke is detected and air quality is Good or Moderate, open with a "
        "brief grounded description of current conditions — do not invent a cause."
    )

    if pm25_mean is None:
        health_instruction = (
            "No ground-level air quality data is available. If smoke is present, note "
            "that residents should monitor official air quality reports rather than "
            "providing specific health guidance."
        )
    else:
        health_instruction = "Gives clear health guidance appropriate to the PM2.5 level"

    sections = []

    sections.append(
        "You are writing a compelling narrative for SmokeStory — an AI-powered "
        "wildfire smoke tool for California journalists and communities.\n\n"
        f"Location: {county_name} County, California\n"
        f"Date: {formatted_date}\n"
        f"PM2.5 level: {pm25_info}\n"
        f"Smoke: {smoke_info}"
    )

    if pm25_mean is not None:
        sections.append(
            f"IMPORTANT: The PM2.5 level is classified as {severity}. "
            "Use this exact classification in your narrative — do not reclassify "
            "the air quality based on your own judgment."
        )

    if news_section:
        sections.append(news_section)

    warning = county_data.get("data_quality_warning")
    if warning:
        sections.append(
            f"DATA QUALITY NOTE: {warning}\n"
            "Because of this, do NOT state that air quality is safe or good based solely "
            "on the PM2.5 reading. Acknowledge that monitoring data may be incomplete and "
            "recommend users verify with official sources."
        )

    sections.append(
        "If the news context contradicts the air quality data, prioritize the data. "
        "Do not imply conditions that contradict the PM2.5 classification. "
        "If news describes events more severe than the classification suggests, "
        "acknowledge the event but anchor all health guidance strictly to the "
        "PM2.5 classification provided."
    )

    sections.append(
        f"Write a 4-sentence narrative that:\n"
        f"- {opening_instruction}\n"
        f"- Connects the event to the specific air quality data\n"
        f"- {health_instruction}\n"
        f"- Ends with one sentence of broader context or what this means for the community\n\n"
        f"Tone: Journalistic but accessible. Factual but human.\n"
        f"Do NOT start with \"On [date]\". Do NOT use bullet points.\n"
        f"Write flowing prose that reads like a news story opening paragraph."
    )

    prompt = "\n\n".join(sections)

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=450,
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
