# Skill: Environmental Narrative Generation

How to use Claude to produce compelling journalism from environmental sensor data — not boilerplate health advisories. Derived from the SmokeStory wildfire smoke tracker project (`narrative/generator.py`, `pipeline/news.py`, `api/main.py`).

---

## 1. The Core Principle: Story First, Data Second

The goal is to make environmental data feel like news, not a warning label.

**Wrong (health advisory framing):**
> PM2.5 is 44.8 µg/m³. Air quality is in the Unhealthy for Sensitive Groups range. People with heart or lung disease, older adults, and children should reduce prolonged or heavy outdoor exertion.

**Right (journalism framing):**
> Fierce wildfires tore through Los Angeles County as authorities ordered mass evacuations across the region, sending a thick curtain of smoke over millions of residents. The air grew measurably dangerous — EPA monitors recorded a daily average of 44.85 micrograms of fine particles per cubic meter, well into territory where even healthy adults can feel effects. Those with asthma or heart conditions should stay indoors and keep windows sealed; outdoor exercise is inadvisable for everyone. For a county that has battled its worst fire seasons back-to-back, Tuesday was another grim chapter in California's worsening climate reality.

**The difference:** The journalism version opens with *why* the air is bad, not *how* bad it is. Data is the evidence for a story that already has a protagonist (the fire, the community, the season).

---

## 2. The 4-Sentence Narrative Structure

Every narrative follows this structure — one sentence per beat:

```
Sentence 1 — The Human Story
  Open with the event or cause, not the measurement.
  Use news headlines if available. Name the fire, the evacuation, the event.

Sentence 2 — Connect to Data
  Now introduce the number, but in plain language.
  "EPA monitors recorded..." / "fine particles reached..." — never bare "PM2.5 is..."

Sentence 3 — Health Guidance (scaled to severity)
  What should people actually do? Scale the urgency to the actual level.
  Name specific groups when relevant. Be direct, not bureaucratic.

Sentence 4 — Broader Context
  Zoom out. Historical comparison, season, trend, community impact.
  This is what makes a story feel significant, not just timely.
```

**Implementation in `generate_narrative()`:**
```python
prompt = f"""Write a 4-sentence narrative that:
- Opens with the human story or event causing the smoke (use news context if available)
- Connects the event to the specific air quality data
- Gives clear health guidance appropriate to the PM2.5 level
- Ends with one sentence of broader context or what this means for the community

Tone: Journalistic but accessible. Factual but human.
Do NOT start with "On [date]". Do NOT use bullet points.
Write flowing prose that reads like a news story opening paragraph."""
```

---

## 3. Integrating News Headlines into Prompts

### Guardian API Pattern

```python
# pipeline/news.py
GUARDIAN_API_KEY = os.getenv("GUARDIAN_API_KEY", "test")

def get_news_headlines(county_name, date):
    # Convert YYYYMMDD → YYYY-MM-DD for Guardian API
    formatted_date = f"{date[:4]}-{date[4:6]}-{date[6:]}"

    params = {
        "q": f"{county_name} wildfire smoke California",
        "from-date": formatted_date,
        "to-date": formatted_date,        # same-day search for historical accuracy
        "order-by": "relevance",
        "page-size": 3,                   # 3 headlines is enough context
        "api-key": GUARDIAN_API_KEY,
        "show-fields": "headline,trailText",
    }
    response = requests.get("https://content.guardianapis.com/search", params=params)
    results = response.json().get("response", {}).get("results", [])
    return [
        {
            "title": r.get("fields", {}).get("headline") or r.get("webTitle"),
            "source": "The Guardian",
            "url": r.get("webUrl"),
        }
        for r in results
    ]
```

**Notes:**
- `"test"` is a valid Guardian API key for low-volume requests (throttled but functional)
- Search on the same date as the data — historical queries only return articles from that exact day
- `show-fields=headline,trailText` — the `headline` field is the edited display title; `webTitle` is the fallback when `headline` is absent
- Query combines county name + `"wildfire smoke California"` — specific enough to avoid noise, broad enough to catch regional coverage

### Injecting Headlines as Context, Not Quotes

Headlines are given to the model as *situational context*, not as text to reproduce verbatim:

```python
# narrative/generator.py
if headlines:
    lines = "\n".join(
        f"- \"{h['title']}\" ({h['source']})" for h in headlines
    )
    news_section = f"Relevant news headlines from this date:\n{lines}\n"
```

The prompt then reads: `{news_section}` followed immediately by the writing instructions. This positions headlines as background briefing — the model synthesizes them into the opening sentence rather than quoting or paraphrasing them directly.

**What to tell the model about headlines:**
- Label them clearly: `"Relevant news headlines from this date:"` — the word *relevant* signals these are for context, not for citation
- List with source attribution — the model uses sourcing as a credibility signal
- Place the news section *before* the writing instructions — it frames the task

### Graceful Fallback When No Headlines Are Available

```python
news_section = ""           # default: empty string
if date:
    headlines = get_news_headlines(county_name, date)
    if headlines:           # only populate if non-empty list
        lines = "\n".join(...)
        news_section = f"Relevant news headlines from this date:\n{lines}\n"

# news_section is either populated or an empty string ""
# The prompt works either way — Claude falls back to data-only narrative
prompt = f"""...
{news_section}
Write a 4-sentence narrative..."""
```

When `news_section` is empty, the model writes from sensor data alone — it opens with what the data implies ("a thick haze settled over...") rather than a named event. The 4-sentence structure still holds; sentence 1 shifts from *event* to *condition* framing.

---

## 4. Severity Scaling — Tone Across AQI Levels

The prompt instructs the model to give "health guidance appropriate to the PM2.5 level." The model infers the correct urgency from the raw µg/m³ value. These are the expected tone profiles by level:

| PM2.5 (µg/m³) | AQI Category | Tone | Health Guidance Style |
|---|---|---|---|
| 0–12 | Good | Calm, reassuring | "Air quality is clean today" — no action needed |
| 12–35 | Moderate | Mild, observational | Note conditions exist; unusually sensitive people may want to limit time outdoors |
| 35–55 | USG (Unhealthy for Sensitive Groups) | Specific, named groups | Name groups explicitly: children, elderly, people with asthma or heart conditions |
| 55–150 | Unhealthy | Direct, action-oriented | "Stay indoors," "avoid outdoor exercise" — applies to everyone, not just sensitive groups |
| 150+ | Very Unhealthy / Hazardous | Urgent, emergency framing | "Close all windows," "use air purifiers," "leave the area if possible" — treat as a public health emergency |

**Implementation note:** The PM2.5 value is passed to the model as `{pm25_mean:.2f} µg/m³ (daily average from EPA ground monitors)`. The model has sufficient training knowledge to map this to AQI categories and calibrate tone accordingly — no explicit AQI category lookup is needed in code. If you want deterministic scaling, map the value in code and add a `severity` field to the prompt.

**Example prompt addition for explicit severity scaling:**
```python
def _severity_label(pm25):
    if pm25 is None:   return "unknown"
    if pm25 < 12:      return "good"
    if pm25 < 35:      return "moderate"
    if pm25 < 55:      return "unhealthy for sensitive groups"
    if pm25 < 150:     return "unhealthy for all"
    return "hazardous"

# Add to prompt:
# f"Air quality severity: {_severity_label(pm25_mean)}\n"
```

---

## 5. The Chat Assistant Pattern

The `/chat` endpoint lets users ask follow-up questions about a county's conditions. The full county context is passed on every message — there is no session state.

```python
# api/main.py
class ChatRequest(BaseModel):
    question: str
    county_data: dict      # the full county object from the map click

@app.post("/chat")
async def chat(body: ChatRequest):
    county = body.county_data
    prompt = f"""You are a helpful air quality assistant for SmokeStory.

County context:
- County: {county.get("county_name")}, state FIPS {county.get("state")}
- Smoke present: {county.get("has_smoke")}
- Smoke density: {county.get("smoke_density")}
- PM2.5 mean: {county.get("pm25_mean")}

User question: {body.question}

Answer in plain English, keeping your response concise and accessible."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return {"answer": message.content[0].text}
```

**Key patterns:**

1. **Pass structured context, not prose** — list county fields explicitly so the model can reference specific values rather than interpolating from a paragraph

2. **Ground answers in actual data** — the prompt provides real numbers; instruct the model to reference them, not speak in generalities. The phrase "Answer in plain English" is load-bearing: it prevents the model from defaulting to clinical language

3. **Keep `max_tokens` low** — 300 tokens forces concision. Chat answers should be 2–4 sentences, not essays. Users asking follow-ups want a direct answer, not a new narrative

4. **No session state needed** — the county data object is cheap to pass on every request. This is simpler than maintaining conversation history and keeps answers grounded in the current view

5. **Frontend sends `county_data` from the last clicked feature** — properties come directly from the GeoJSON `feat.properties` object:
```javascript
// frontend sends:
fetch(`${API}/chat`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ question: userInput, county_data: feat.properties })
})
```

---

## 6. What NOT To Do

These are explicit anti-patterns, some enforced in the prompt, others learned from iteration:

### Never start with "On [date]"
```python
# Enforced in the prompt:
"Do NOT start with 'On [date]'."
```
"On January 9, 2025, wildfires broke out..." is the most generic possible opening. It buries the story under a dateline. Start with action or condition instead.

### Never use bullet points in narratives
```python
"Do NOT use bullet points."
```
Bullets signal a list of facts, not a story. A narrative must flow as prose — each sentence must follow from the last. If you get bullets, the model has defaulted to advisory mode.

### Never say "PM2.5 levels" without explaining what that means
Bare jargon alienates the non-expert reader. Always pair with a plain-language gloss:

| Instead of | Write |
|---|---|
| "PM2.5 levels reached 44.8" | "fine particle pollution reached 44.85 micrograms per cubic meter" |
| "The AQI is 150" | "air quality reached a level health officials call Unhealthy" |
| "PM2.5 exceeded the NAAQS standard" | "pollution surpassed the federal health limit" |

The raw number in µg/m³ is passed to the model; it is the model's job to translate it for the reader. The prompt does not need to do this translation — but it should not call the number "PM2.5 levels" in the instructions, as that phrase leaks through into model output.

### Never produce a health advisory when a story is possible
If news headlines are available, the model must use them. A prompt that says "write a narrative" while providing headlines and then getting back generic advisory language is a prompt failure — usually caused by putting instructions before context. Structure matters:

```python
# Wrong order — model ignores news, falls back to advisory
prompt = f"""Write a 4-sentence narrative. Be journalistic.
Location: {county_name}
PM2.5: {pm25_info}
Relevant news: {news_section}"""   # ← news comes after instructions

# Right order — news primes the model before the writing task
prompt = f"""Location: {county_name}
PM2.5: {pm25_info}
{news_section}
Write a 4-sentence narrative..."""  # ← instructions come after context
```

### Never use more than 300 tokens for a 4-sentence narrative
`max_tokens=300` is a deliberate constraint. Narratives that exceed this have drifted into explanation or over-qualification. If the model is producing 5+ sentences, tighten the prompt instruction: "Write exactly 4 sentences."

---

## 7. Reusable Prompt Template for Environmental Hazards

This template generalizes the SmokeStory pattern to other environmental hazards: flood risk, heat islands, earthquake exposure, drought conditions, etc.

```python
def generate_environmental_narrative(
    location: str,           # "Napa County, California"
    date_str: str,           # "January 9, 2025"
    hazard_type: str,        # "wildfire smoke" | "flood" | "extreme heat" | "drought"
    primary_metric: str,     # "PM2.5: 44.85 µg/m³" | "Flood stage: 32.4 ft (major)"
    secondary_metric: str,   # "Smoke density: Heavy" | "Rainfall: 3.2 in (48hr)"
    news_headlines: list,    # [{"title": "...", "source": "..."}] or []
    severity: str,           # "good" | "moderate" | "elevated" | "severe" | "extreme"
    model: str = "claude-sonnet-4-20250514",
    max_tokens: int = 300,
) -> str:

    # Build news context block
    if news_headlines:
        news_lines = "\n".join(
            f"- \"{h['title']}\" ({h['source']})" for h in news_headlines
        )
        news_section = f"Relevant news headlines from this date:\n{news_lines}\n\n"
    else:
        news_section = ""

    # Severity → action language map
    action_guidance = {
        "good":     "No protective action is needed.",
        "moderate": "Unusually sensitive people may want to limit prolonged outdoor exposure.",
        "elevated": "Sensitive groups — children, elderly, those with respiratory or heart conditions — should reduce outdoor time.",
        "severe":   "Everyone should avoid prolonged outdoor exertion. Sensitive groups should stay indoors.",
        "extreme":  "This is a public health emergency. Stay indoors, seal windows, and follow official evacuation or shelter-in-place orders.",
    }
    guidance_hint = action_guidance.get(severity, "Follow guidance from local health officials.")

    prompt = f"""You are a journalist writing a brief narrative for a data-driven environmental monitoring tool.

Location: {location}
Date: {date_str}
Hazard: {hazard_type}
{primary_metric}
{secondary_metric}
Severity level: {severity}
Health guidance context: {guidance_hint}

{news_section}Write a 4-sentence narrative that:
1. Opens with the human story or event behind the conditions (use news context if available; if not, describe the conditions as a lived experience)
2. Connects the event to the specific measurement data — translate numbers into plain English
3. Gives clear, proportionate health or safety guidance for this severity level
4. Ends with one sentence of broader context: historical, seasonal, or community significance

Rules:
- Do NOT start with "On [date]"
- Do NOT use bullet points or lists
- Do NOT reproduce technical jargon without a plain-language explanation
- Write flowing prose, like the opening of a news article
- Be factual and grounded in the data provided — do not speculate"""

    client = anthropic.Anthropic()
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text
```

### Example calls for other hazards:

```python
# Flood risk
generate_environmental_narrative(
    location="Sacramento County, California",
    date_str="February 14, 2024",
    hazard_type="river flooding",
    primary_metric="American River stage: 34.2 ft (flood stage: 25 ft)",
    secondary_metric="48-hour rainfall: 4.8 inches",
    news_headlines=headlines,
    severity="severe",
)

# Extreme heat
generate_environmental_narrative(
    location="Fresno County, California",
    date_str="July 10, 2024",
    hazard_type="extreme heat",
    primary_metric="High temperature: 114°F (heat index: 118°F)",
    secondary_metric="Consecutive days above 100°F: 8",
    news_headlines=headlines,
    severity="extreme",
)

# Drought
generate_environmental_narrative(
    location="Sonoma County, California",
    date_str="September 1, 2021",
    hazard_type="drought and water shortage",
    primary_metric="Reservoir storage: 18% of capacity",
    secondary_metric="Palmer Drought Severity Index: -4.2 (Extreme Drought)",
    news_headlines=headlines,
    severity="elevated",
)
```

---

## Quick Reference

### Prompt construction order (matters)
```
1. Role/persona sentence
2. Location, date, hazard type
3. Measurements (plain-language labels)
4. News headlines (if any)
5. Writing instructions
6. Explicit prohibitions
```

### Data formatting for prompts
```python
# Always format the number with units and source
f"{pm25_mean:.2f} µg/m³ (daily average from EPA ground monitors)"
# NOT: f"PM2.5: {pm25_mean}"

# Smoke density in lowercase
f"Smoke is present with {smoke_density.lower()} density."

# Formatted date for human readability
datetime.strptime(date, "%Y%m%d").strftime("%B %-d, %Y")  # "January 9, 2025"
```

### Guardian API date format
```python
# Input:  "20250109"  (YYYYMMDD)
# Output: "2025-01-09" (YYYY-MM-DD, Guardian format)
formatted_date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
```

### Model settings for narratives
```python
model = "claude-sonnet-4-20250514"   # Sonnet: right balance of quality and speed
max_tokens = 300                      # ~4 sentences; force concision
```

### Signs the prompt is failing
| Symptom | Fix |
|---|---|
| Output starts with "On [date]" | Add explicit prohibition to prompt |
| Output uses bullet points | Add "Do NOT use bullet points" to rules |
| Output ignores headlines | Move news section before writing instructions |
| Output is a health advisory | Add "journalistic" to tone instruction; verify news_section is non-empty |
| Output is 6+ sentences | Add "Write exactly 4 sentences" |
| Output says "PM2.5 levels" | Instruct model to translate jargon; label data as "fine particle pollution" in prompt |
