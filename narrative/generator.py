import os
import anthropic
from datetime import datetime
from dotenv import load_dotenv

from pipeline.news import get_news_headlines

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SAFE_DAILY_LIMIT = 35.4  # EPA 24-hour standard (µg/m³)


def get_severity_label(pm25):
    # AQI breakpoints per 2024 EPA revision (effective May 2024)
    # Annual NAAQS lowered to 9 µg/m³; 24-hr standard unchanged at 35 µg/m³
    if pm25 is None:
        return None
    if pm25 <= 9.0:
        return "Good"
    elif pm25 <= 35.4:
        return "Moderate"
    elif pm25 <= 55.4:
        return "Unhealthy for Sensitive Groups"
    elif pm25 <= 125.4:
        return "Unhealthy"
    elif pm25 <= 225.4:
        return "Very Unhealthy"
    else:
        return "Hazardous"


def humanize_pm25(pm25):
    """Express PM2.5 relative to the EPA safe daily limit."""
    if pm25 is None or pm25 <= SAFE_DAILY_LIMIT:
        return None
    ratio = pm25 / SAFE_DAILY_LIMIT
    if ratio < 1.5:
        return "just above the EPA safe daily limit"
    elif ratio < 2.0:
        return f"about {ratio:.1f}x the EPA safe daily limit"
    elif ratio < 3.0:
        return f"nearly {round(ratio)}x the EPA safe daily limit"
    else:
        return f"more than {int(ratio)}x the EPA safe daily limit"


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
        human_scale = humanize_pm25(pm25_mean)
        if human_scale:
            pm25_info = (
                f"{pm25_mean:.1f} µg/m³ ({human_scale}) — "
                f"classified as {severity} by EPA standards"
            )
        else:
            pm25_info = f"{pm25_mean:.1f} µg/m³ — classified as {severity} by EPA standards"
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

    # ── News context ───────────────────────────────────────────
    news_section = ""
    if date:
        headlines = get_news_headlines(county_name, date)
        if headlines:
            lines = []
            for h in headlines:
                line = f"- Headline: \"{h['title']}\""
                if h.get("summary"):
                    line += f"\n  Summary: {h['summary']}"
                line += f" ({h['source']})"
                lines.append(line)
            news_section = (
                "Guardian news context for this date (use specific facts from these "
                "articles to ground the narrative — do not invent details not present here):\n"
                + "\n".join(lines)
            )

    # ── Sentence-level instructions ────────────────────────────
    if pm25_mean is None:
        health_instruction = (
            "Sentence 3 — Health guidance: No PM2.5 monitor data is available. "
            "If smoke is present, note that residents should check AirNow.gov rather than "
            "stating specific health guidance."
        )
    else:
        health_instruction = (
            f"Sentence 3 — Health guidance: Give concrete guidance matched to the "
            f"{severity} classification. Name who is most at risk. Recommend a specific action."
        )

    opening_instruction = (
        "Sentence 1 — Opening: Choose ONE mode and commit to it:\n"
        "  (a) A specific place, neighborhood, or landmark from the news context\n"
        "  (b) A concrete environmental condition grounded in the data\n"
        "  (c) A human action or impact drawn directly from the news\n"
        "  (d) A contrast — what's normal vs. what's happening now\n"
        "Do NOT open with a generalization. Do NOT open with 'On [date]' or '[County] County'."
    )

    sections = []

    # ── Persona and accuracy rules ─────────────────────────────
    sections.append(
        "You are a senior environmental reporter at the LA Times writing a dispatch on deadline. "
        "You write with precision — every specific claim (names, places, numbers, events) must be "
        "traceable to the data or Guardian context provided below. "
        "Do not invent specific details, locations within the county, or events not mentioned "
        "in the source material. If no news context is available, stay strictly with what "
        "the data tells you.\n\n"
        f"Location: {county_name} County, California\n"
        f"Date: {formatted_date}\n"
        f"PM2.5: {pm25_info}\n"
        f"Smoke: {smoke_info}"
    )

    if pm25_mean is not None:
        sections.append(
            f"IMPORTANT: The PM2.5 level is classified as {severity}. "
            "Use this exact classification — do not reclassify based on your own judgment."
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
        "Write a 4-sentence narrative structured as follows:\n\n"
        f"{opening_instruction}\n\n"
        f"Sentence 2 — Data: Connect the event to the PM2.5 reading. "
        f"Express the number in human terms (e.g., 'X times the safe daily limit') "
        f"not just the EPA label. If the number is below the safe threshold, say so plainly.\n\n"
        f"{health_instruction}\n\n"
        "Sentence 4 — Context: One sentence of broader context about wildfire, smoke, "
        "air quality, or climate as it relates to this county or California. "
        "Do NOT reference unrelated news events (crime, politics, sports, etc.).\n\n"
        "Geographic rule: If you use a specific city, neighborhood, or location name "
        f"from the news context in sentence 1, it must be within {county_name} County. "
        "If a Guardian article describes a location in a different county, you may reference "
        "the event as broader California context (sentences 2 or 4 only) — never as a "
        "sentence 1 anchor for this county.\n\n"
        "Writing rules:\n"
        "  - Health guidance must name a specific population at risk and a specific action "
        "to take. Do not write it as a public health advisory ('residents are urged', "
        "'officials warn', 'health authorities recommend', 'it is important to'). "
        "Write it as a direct, concrete statement.\n"
        "  - Do not open with '[density] smoke blankets [county]' — this restates the "
        "input data, not a scene. Choose a real opening mode from the list above.\n\n"
        "Output all four sentences as a single paragraph with no line breaks between sentences. "
        "Write flowing prose. No bullet points. Each sentence should be distinct and load-bearing."
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
