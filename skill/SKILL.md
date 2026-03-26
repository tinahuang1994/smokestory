# Climate Data Narrative Skill
## How to Build a Geospatial Climate Intelligence Tool
### Reference Implementation: SmokeStory

Built by Tina Huang · tina.huang@aya.yale.edu
Reference project: https://smokestory.onrender.com
GitHub: https://github.com/tinahuang1994/smokestory

---

## WHO THIS SKILL IS FOR

This skill is for three audiences:

DEVELOPERS
You want to build your own version of SmokeStory for a different climate disaster or region. This skill gives you the architecture patterns, code templates, and deployment lessons from SmokeStory so your numbers are trustworthy.

SCIENCE COMMUNICATORS
You want to publish findings about a climate event in a way that is accurate and legible to a general audience. This skill explains every methodological choice in plain language.

CLIMATE RESEARCHERS
You want to adapt the financial impact methodology or narrative engine for your own analysis. This skill documents the scientific frameworks used and their limitations.

---

## WHAT YOU CAN BUILD WITH THIS SKILL

SmokeStory implements a three-layer architecture that can be adapted for other climate disasters with geospatial data.

Layer 1 — DATA PIPELINE
Fetch raw satellite and sensor data from government APIs, spatially join it to administrative boundaries, and clean it for display and narrative generation.

Layer 2 — NARRATIVE ENGINE
Convert structured location-level data into calibrated plain-English AI narratives using Claude, with severity-appropriate tone and scientifically grounded guidance.

Layer 3 — FINANCIAL IMPACT MODULE
Estimate three independent economic impacts using actuarial, real estate economics, and environmental health economics frameworks.

POSSIBLE ADAPTATIONS:
The three-layer architecture can in principle be adapted for other climate hazards where:
- Geospatial hazard data exists (satellite, sensor, or model output)
- Administrative boundary data is available (county, zip code, census tract)
- A severity classification system exists (EPA AQI, NWS warning levels, USGS flood stages)

Examples of hazard types where this pattern may apply include floods, drought, heat waves, hurricanes, and air quality events beyond wildfire.

NOTE: SmokeStory has only been built and validated for wildfire smoke in California. Adapting it for other hazards will require identifying appropriate data sources, validating severity thresholds, and testing the narrative output for that specific domain. The patterns here are starting points, not verified implementations for other hazards.

---

## PART 1: DATA PIPELINE

### 1.1 Core Architecture Principles

These principles were learned through building and deploying SmokeStory. They apply regardless of what hazard type you are building for.

PRINCIPLE 1: Never cache to disk in production.
Render and similar free-tier platforms reset the filesystem on every deploy. Always fetch data from URLs at request time. Never write files to disk and expect them to persist between deploys or requests.

WRONG approach:
  Save a file to disk on first request,
  read it back on subsequent requests.
  This breaks silently on Render after deploy.

RIGHT approach:
  Fetch from the source URL on every request,
  process it in memory, return the result.
  Use BytesIO to read files without writing to disk.

PRINCIPLE 2: Use verify=False for government URLs.
Many US government data endpoints (.gov, .noaa.gov, .nasa.gov) have SSL certificate issues on cloud platforms. Add verify=False to all government API requests.

  resp = requests.get(url, verify=False, timeout=30)

PRINCIPLE 3: Sanitize NaN before JSON serialization.
Python float NaN is not valid JSON. Spatial joins produce NaN for counties with no matching data. Always sanitize before returning from any endpoint.

  def safe_val(v):
      if v is None:
          return None
      try:
          if math.isnan(float(v)):
              return None
      except:
          pass
      return v

PRINCIPLE 4: Be consistent between map and narrative.
If your map shows county-level averages, your narrative endpoint must use the same aggregation method. Inconsistency (map shows mean, narrative uses max) produces contradictory numbers that undermine user trust. Choose one method and label it clearly.

PRINCIPLE 5: Validate dates at the API level.
Add input guards to reject dates before your earliest available data and after today. Return HTTP 400 with a clear message rather than silently returning empty data.

  from datetime import date, datetime

  def validate_date(date_str):
      try:
          d = datetime.strptime(date_str, "%Y%m%d").date()
      except ValueError:
          raise HTTPException(400,
              "Invalid date format. Use YYYYMMDD.")
      if d < date(2005, 8, 1):
          raise HTTPException(400,
              "No data before August 2005.")
      if d > date.today():
          raise HTTPException(400,
              "Date cannot be in the future.")
      return d

### 1.2 The Spatial Join Pattern

The core operation in every pipeline is joining point or polygon hazard data to administrative boundaries.

This pattern works for any hazard type:

  import geopandas as gpd
  import pandas as pd
  import requests
  import io

  # Step 1: Load county/admin boundaries from URL
  # Never cache this file to disk
  resp = requests.get(BOUNDARIES_URL, verify=False)
  boundaries = gpd.read_file(
      io.BytesIO(resp.content)
  )
  boundaries = boundaries.to_crs('EPSG:4326')

  # Step 2: Load hazard point data
  hazard_points = gpd.GeoDataFrame(
      df,
      geometry=gpd.points_from_xy(df.lon, df.lat),
      crs='EPSG:4326'
  )

  # Step 3: Spatial join
  joined = gpd.sjoin(
      boundaries,
      hazard_points,
      how='left',
      predicate='intersects'
  )

  # Step 4: Aggregate by administrative unit
  # Choose mean or max based on your use case
  # and document the choice clearly
  result = joined.groupby(
      'admin_name'
  )['value'].mean()

For California county boundaries specifically, the Code for America GeoJSON works well and is fetched at runtime:
https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/california-counties.geojson

For other states, Census TIGER boundary files are the standard source.

### 1.3 Data Sources for Wildfire/Smoke

These are the specific sources used in SmokeStory, verified and working as of early 2025:

Active fires: NASA FIRMS VIIRS
  Free API key required
  Supports near-real-time and archive modes
  Returns fire detections with Fire Radiative Power

Smoke plumes: NOAA Hazard Mapping System (HMS)
  No authentication required
  Daily shapefiles by date
  Light/Medium/Heavy density classification

Air quality: EPA Air Quality System (AQS)
  Free registration required
  Parameter 88101 for PM2.5 (FRM/FEM monitors)
  Returns daily mean by monitor location

NOTE: For hazard types other than wildfire smoke, you will need to identify equivalent data sources appropriate to that domain. The patterns above (point data with intensity, polygon data with severity class, ground sensor readings by location) are the right types of data to look for — but the specific sources will vary and should be validated before use.

### 1.4 Known Data Quality Issues

These issues were discovered in production and apply to the SmokeStory data sources:

EPA AQS monitor outages during disasters:
During major fire events, EPA ground monitors sometimes go offline due to evacuation or power loss. This produces anomalously low PM2.5 readings for the most affected counties — the opposite of the true situation. Always cross-reference with satellite smoke density when PM2.5 seems too low.

Detection logic used in SmokeStory:
  if has_smoke and pm25 is not None and pm25 < 15:
      flag as potentially incomplete data

AQS data recency lag:
AQS data for recent dates is preliminary. Final quality-assured data typically takes 2–6 months. For dates within 90 days, add a note that data may be updated.

HMS smoke vs ground-level air quality:
NOAA HMS polygons show atmospheric smoke detected by satellite. This does not always correspond to ground-level air quality — smoke at altitude may not reach the surface, or may be more concentrated at ground level than the satellite shows. Always present these as two separate measurements.

---

## PART 2: NARRATIVE ENGINE

### 2.1 Core Principles

PRINCIPLE 1: Never let the AI classify severity.
Always calculate the severity label in Python using the exact same thresholds as your frontend, then pass the label explicitly to the model. Claude will use its training knowledge to independently classify severity if you don't, and its thresholds may differ from yours or from the current regulatory standard.

WRONG:
  prompt = f"PM2.5 is {pm25}. Write a narrative."

RIGHT:
  severity = get_severity_label(pm25)
  prompt = f"""
  PM2.5 is {pm25} µg/m³, classified as {severity}.
  IMPORTANT: Use this exact classification.
  Do not reclassify based on your own judgment.
  """

PRINCIPLE 2: Keep narrative and data in sync.
If the data card shows 44.8 µg/m³, the narrative must reference 44.8 µg/m³ — not a different value from a separate API call. Pass the exact value from the data response into the narrative prompt.

PRINCIPLE 3: Pass data quality warnings to the model.
If your underlying data is suspect, tell Claude:

  if data_quality_warning:
      prompt += f"""
      DATA QUALITY NOTE: {data_quality_warning}
      Do not assert conditions are safe or normal.
      Acknowledge data may be incomplete.
      """

PRINCIPLE 4: Add medical disclaimers to health responses.
Any chat interface answering health questions should always append:
  "For medical advice, consult your doctor or local health authority."

PRINCIPLE 5: Use higher max_tokens than you think.
A 4-sentence journalistic narrative with news context can exceed 300 tokens. Use 400–500 to avoid silent truncation. Check stop_reason in the response — if it is not "end_turn", the narrative was cut off.

### 2.2 Severity Label Function

Use current EPA PM2.5 thresholds (revised February 2024). These replaced the previous thresholds where Good was 0–12 µg/m³.

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

Apply this same function in both the backend (for the narrative) and the frontend JavaScript (for the UI badge). If they differ, users will see contradictory classifications.

### 2.3 Four-Sentence Narrative Structure

This prompt structure produces consistently calibrated journalistic narratives:

  """
  Write a 4-sentence narrative for {county} County,
  California on {date}.

  Data:
  - PM2.5: {pm25} µg/m³ — classified as {severity}
  - Smoke: {smoke_info}
  - News context: {headlines}

  IMPORTANT: {severity} is the correct
  classification. Use it. Do not reclassify.

  If news contradicts the data, prioritize the
  data. Do not imply conditions that contradict
  the PM2.5 measurement.

  Structure:
  Sentence 1: If smoke or fire is present, open
  with the human story behind it. If no smoke and
  Good/Moderate air, describe current conditions
  without inventing a cause.

  Sentence 2: The data — PM2.5 value, severity
  classification, smoke density if present.

  Sentence 3: Health guidance appropriate to
  {severity}. Use the classification provided.

  Sentence 4: Broader context or outlook.

  Write in a journalistic style, not an advisory
  style. Use active voice.
  """

### 2.4 Severity-Tone Mapping

Calibrate the narrative tone to severity:

  Good:
    Tone: calm, reassuring
    Health guidance: no action needed for most people

  Moderate:
    Tone: mild awareness
    Health guidance: unusually sensitive people only

  Unhealthy for Sensitive Groups:
    Tone: clear but not alarming
    Health guidance: name the groups
    (children, elderly, heart/lung conditions)
    Recommend limiting prolonged outdoor activity

  Unhealthy:
    Tone: direct, action-oriented
    Health guidance: everyone may be affected
    Recommend limiting outdoor exertion

  Very Unhealthy:
    Tone: urgent
    Health guidance: everyone should reduce
    outdoor activity significantly

  Hazardous:
    Tone: emergency framing
    Health guidance: avoid all outdoor activity

---

## PART 3: FINANCIAL IMPACT MODULE

### 3.1 The Three-Estimate Framework

The most important design decision in the financial impact module is presenting three independent estimates rather than one total number.

This is not a limitation — it is the methodologically correct approach. These three types of loss measure different things, use different data sources, and cannot be added together without double counting.

ESTIMATE TYPE 1 — DIRECT PHYSICAL DESTRUCTION
What it measures: The market value of structures physically destroyed or damaged.
Data needed:
  - Official damage count by structure type
    (use government inspection data, not estimates)
  - Pre-disaster market values by location
    (use pre-disaster transaction data, not
    post-disaster values which already reflect
    the impact)
Method: Structure count × median market value
Validation: Compare against insurance industry loss estimates for the same event

ESTIMATE TYPE 2 — AREA PROPERTY VALUE IMPACT
What it measures: Estimated decline in property values for structures that survived but are in the affected area.
Data needed:
  - Peer-reviewed academic literature on how
    similar disasters affect nearby property values
  - Estimate of total housing stock in affected zone
Method: Literature-based depreciation rate × affected housing stock value
Important: Use a single literature-anchored value, not an optimistic range. Only extend to a higher value if directly supported by a published source.
Validation: Check against observed post-disaster transaction data, noting that distressed sales may not represent typical properties

ESTIMATE TYPE 3 — HEALTH ECONOMIC COST
What it measures: Economic cost of health impacts from the disaster (hospitalizations, ER visits, missed work, restricted activity).
Data needed:
  - Exposure data (sensor readings or model output)
  - Exposed population count
  - Health impact functions from regulatory literature
Method: EPA BenMAP Cost of Illness methodology
  Step 1: Calculate excess exposure
    (measured value minus safe threshold)
  Step 2: Apply health impact functions
    (incidence rates from EPA BenMAP TSD)
  Step 3: Apply COI unit values
    (EPA BenMAP configuration files)
Note: Use COI (Cost of Illness), not VSL (Value of Statistical Life). VSL is designed for chronic regulatory analysis, not acute events. COI is more defensible for short-duration disasters.
Validation: EPA BenMAP published applications for similar air quality events

### 3.2 What to Write on the Page

HEADLINE NUMBER: Use Estimate 1 only.
It is the most defensible, most auditable, and most quotable by journalists.

THREE CARDS: Show all three estimates independently with clear labels.
Each card must state what it measures and what it does NOT measure.

MUST-NOT-ADD DISCLAIMER: Appear at least twice — once near the headline number and once near the three cards.

EXTERNAL VALIDATION TABLE: Show how your Estimate 1 compares to published estimates from insurance companies, academic institutions, and government agencies. This builds credibility. Note that different sources use different scopes (insured only vs total market value vs full economic impact) — explain the differences.

### 3.3 Science Communication Rules

These rules were developed through multiple rounds of external review for SmokeStory:

RULE 1: Separate three audiences.
The page needs three information layers:
  Layer A (3 seconds): headline number only
  Layer B (30 seconds): three cards with
    plain-language descriptions, expandable
  Layer C (3+ minutes): full methodology
    on a separate /methodology page

RULE 2: Plain language for Layer A and B.
Never use these terms in user-facing content:
  COI → "economic cost of health impacts"
  VSL → do not reference
  quasi-experimental → do not reference
  BenMAP → "the same method the EPA uses"
  DINS → "CAL FIRE field inspections"

RULE 3: Every number needs a scope statement.
"$36B–$40B" is meaningless without
"in structures destroyed, pre-fire market value,
Los Angeles County, January 2025."
Always show scope directly under the number.

RULE 4: Limitations must be visible, not buried.
Do not hide limitations only in the methodology page. The most important limitation for each estimate should appear on the main impact page in an expandable section, not just in the full methodology.

RULE 5: Author attribution matters for journalists.
Include a named human contact (name + email) on the page. Anonymous methodology documents are harder to cite and easier to dismiss.

RULE 6: Separate Claude AI from data sources.
Do not list Claude AI in the same line as NOAA, EPA, and NASA. Journalists will not cite a source that mixes AI with regulatory data agencies. Separate them:
  DATA: NOAA HMS · EPA AQS · NASA VIIRS
  NARRATIVES POWERED BY CLAUDE AI

---

## PART 4: FRONTEND PATTERNS

### 4.1 Map Design Principles

Use a dark basemap (CartoDB Dark Matter or similar). Climate hazard data reads much more dramatically on dark backgrounds — smoke appears more ominous, fire points glow, PM2.5 color scales pop.

Layer order matters:
  Bottom: PM2.5 choropleth (county fills)
  Middle: Smoke/hazard polygons
  Top: Point data (fires, gauges, sensors)

Use Leaflet panes to enforce z-order:
  map.createPane('topPane')
  map.getPane('topPane').style.zIndex = 650

Always add hover tooltips to every clickable layer. Users cannot know what they are clicking without county/feature names on hover. This is the single highest-impact UX improvement for any map interface.

Add cursor: pointer to all interactive layers:
  .leaflet-interactive { cursor: pointer !important; }

### 4.2 Color Scale Principles

For sequential hazard data (more = worse): Use a color scale that is perceptually monotonic and colorblind-safe. The EPA AQI color scale (green → yellow → orange → red → purple) is widely recognized and acceptable despite not being perfectly colorblind-safe.

If colorblind accessibility is a priority, consider a teal → yellow → orange → deep red → near-black scale which performs better under deuteranopia simulation.

Always use the current regulatory thresholds, not historical ones. The EPA revised PM2.5 thresholds in February 2024.

### 4.3 Single-File Frontend Pattern

SmokeStory's entire frontend is one HTML file with inline CSS and JavaScript. This has significant advantages for a small project:

  - No build step required
  - No npm, webpack, or bundler
  - Easy to deploy on any static file server
  - Easy to read and audit
  - FastAPI serves it directly with FileResponse

The tradeoff is that large single files become hard to maintain above ~3,000 lines. Consider splitting into separate CSS and JS files if the project grows beyond that.

---

## PART 5: DEPLOYMENT

### 5.1 Render Free Tier Checklist

These are the lessons learned deploying SmokeStory on Render's free tier:

START COMMAND:
  Must be: uvicorn api.main:app --host 0.0.0.0 --port $PORT
  Never hardcode the port number.
  Always use $PORT.

EPHEMERAL FILESYSTEM:
  Never cache files to disk.
  Never assume a file written in one request
  will exist in the next.
  See Part 1, Principle 1.

COLD STARTS:
  Render free tier sleeps after 15 minutes of inactivity. First request after sleep takes 3–4 seconds extra.
  Use UptimeRobot (free) to ping every 5 minutes and keep the server warm during expected usage.

SSL CERTIFICATES:
  Government URLs require verify=False.
  See Part 1, Principle 2.

ENVIRONMENT VARIABLES:
  Set all API keys in Render dashboard, never in code.
  Use a .env.example file in the repo to document required keys without exposing values.

STATIC FILES:
  Serve HTML files with FastAPI FileResponse:

    from fastapi.responses import FileResponse

    @app.get("/")
    async def index():
        return FileResponse("frontend/index.html")

### 5.2 NaN Serialization Fix

This bug will appear in every geospatial project and is easy to miss. Spatial joins produce NaN for features with no matching data. Python's json module cannot serialize NaN. FastAPI will throw a 500 error when trying to return NaN in a response.

Fix: sanitize all values before returning:

  import math

  def safe_val(v):
      if v is None:
          return None
      try:
          if math.isnan(float(v)):
              return None
      except:
          pass
      return v

Apply this to every numeric field before including it in a response dict.

---

## PART 6: TESTING PATTERNS

### 6.1 The Agent Review Pattern

SmokeStory used a multi-agent review system before publishing. This pattern is reusable for any data product:

Run 5 independent review agents in parallel, each with a different expert persona:

  Agent 1: UX/UI Reviewer
  Agent 2: Science Communication Reviewer
  Agent 3: Journalist Reviewer
  Agent 4: Skeptic Reviewer (finds misuse risks)
  Agent 5: Data Integrity Reviewer
           (verifies every number)

Then run one Chief Reviewer agent that reads all 5 reports, resolves conflicts, and produces a single prioritized action list.

This approach consistently finds issues that a single reviewer misses because each agent approaches the product from a completely different angle.

### 6.2 Data Accuracy Spot Check

Before publishing, manually verify your data against official sources for at least 3 dates:

  - A major event date (worst conditions)
  - A normal date (typical conditions)
  - A historical date at least 2 years ago

For each date, check:
  - Does your county value match official sources?
  - Does the severity classification match
    what official sources show?
  - Do any counties show physically implausible
    values (e.g. monitor at fire origin shows
    Good air quality)?

### 6.3 Narrative Consistency Test

Run the same county and date 3 times and compare:
  - Is the numeric value identical across all 3?
  - Is the severity label identical across all 3?
  - Is the health guidance consistent?
  - Does the tone match the severity level?

If the numeric value differs across runs, your pipeline has a data consistency bug (likely different aggregation methods in different code paths).

---

## APPENDIX: FINANCIAL IMPACT DATA SOURCES

These are the specific sources used for the SmokeStory 2025 LA Wildfire financial impact module. These are provided as examples of the type of data needed, not as a prescriptive list for other disasters.

Structure damage: Government inspection data
  SmokeStory used: CAL FIRE DINS
  Equivalent for other disasters: FEMA damage
  assessments, local building department records

Pre-disaster property values: Transaction data
  SmokeStory used: California Association of
  Realtors 2024 annual median prices
  Equivalent for other disasters: State/county
  realtor associations, Zillow Research CSV data
  (free download, not API)

Property depreciation rate: Academic literature
  SmokeStory used: Sathaye et al. 2024,
  Landscape and Urban Planning
  For other hazards: Search peer-reviewed
  literature for the specific hazard type and
  region — do not assume wildfire depreciation
  rates apply to floods or hurricanes

Health impact functions: EPA BenMAP
  SmokeStory used: EPA BenMAP TSD January 2023
  (EPA-HQ-OAR-2020-0272)
  These functions are specific to PM2.5.
  Other hazards need different health impact
  functions appropriate to that exposure type.

COI unit values: EPA BenMAP configuration files
  Available at epa.gov/benmap
  Updated periodically — always use current version

---

## LIMITATIONS OF THIS SKILL

This skill documents what was built and learned in SmokeStory. It is not a comprehensive textbook on geospatial data science or environmental economics.

Specific limitations:

1. SmokeStory has only been validated for wildfire smoke in California. The patterns here may need significant modification for other hazard types or geographies.

2. The financial impact methodology is a consulting-style estimate, not an actuarial or academic model. It is appropriate for public communication but should not be used for insurance or legal purposes.

3. The data sources listed are current as of early 2025. Government APIs change URLs, formats, and access requirements without notice. Always verify URLs before building.

4. The narrative patterns were developed for US English language output targeting journalists and lay readers. Adapting for other languages, cultures, or professional audiences will require prompt re-engineering.

5. Render free tier has significant limitations (ephemeral filesystem, cold starts, single worker). For production use with multiple concurrent users, a paid hosting tier or different platform is recommended.

---

## QUICK REFERENCE

Key Python packages:
  geopandas — spatial joins and GeoJSON handling
  fastapi — API framework
  anthropic — Claude API client
  requests — HTTP fetching with verify=False
  pandas — data manipulation
  uvicorn — ASGI server

Key gotchas:
  Always verify=False for .gov URLs
  Always safe_val() before JSON serialization
  Always pass severity label to Claude explicitly
  Always fetch county boundaries from URL,
    never cache to disk
  Always use $PORT in Render start command
  Always use pre-disaster property values,
    not post-disaster

Key thresholds (PM2.5, 2024 EPA standard):
  Good: 0–9.0 µg/m³
  Moderate: 9.1–35.4 µg/m³
  Unhealthy for Sensitive Groups: 35.5–55.4 µg/m³
  Unhealthy: 55.5–150.4 µg/m³
  Very Unhealthy: 150.5–250.4 µg/m³
  Hazardous: 250.5+ µg/m³
