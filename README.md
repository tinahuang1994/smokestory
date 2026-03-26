# SmokeStory
### AI-Powered Wildfire Smoke Intelligence for California

> Translating raw satellite and sensor data into plain-English narratives for journalists, researchers, and communities affected by California's wildfires.

Live site: https://smokestory.onrender.com
Built by: Tina Huang · tina.huang@aya.yale.edu
GitHub: https://github.com/tinahuang1994/smokestory

---

## What It Does

SmokeStory combines three real-time satellite and sensor data sources to tell the story of wildfire smoke:

- **Where the fires are** — NASA VIIRS satellite fire detections with Fire Radiative Power (FRP) intensity data
- **Where the smoke is** — NOAA Hazard Mapping System smoke plume boundaries with density classification
- **How bad the air is** — EPA Air Quality System PM2.5 ground monitor readings by county

For any California county on any date since 2005, SmokeStory generates a plain-English AI narrative combining all three data sources — calibrated to the severity of conditions and grounded in the actual sensor readings.

---

## Features

### Interactive Map
- Three toggleable data layers: PM2.5 counties, smoke plumes, active fire points
- Hover tooltips showing county name and PM2.5 value
- Click any county to open the data panel
- 8 historic wildfire events pre-loaded for exploration
- Covers August 2005 to present

### AI Narrative Generation
- 4-sentence journalistic narrative per county per date
- Severity-calibrated language (Good through Hazardous)
- Integrates Guardian news headlines for context
- Powered by Claude claude-sonnet-4-20250514
- Explicit EPA severity classification passed to model — no independent AI reclassification

### Financial Impact Module
Estimates the economic impact of the January 2025 Palisades and Eaton Fires on Los Angeles County. Three independent estimates shown separately — these figures must not be added together:

**Estimate 01 — Direct Property Destruction: $36B – $40B**
What it measures: Market value of 16,249 destroyed structures.
Source: CAL FIRE DINS × CAR 2024 prices.

**Estimate 02 — Neighborhood Value Impact: $3.9B**
What it measures: Property value decline within 5 miles of fire perimeters.
Source: Sathaye et al. 2024, Landscape and Urban Planning.

**Estimate 03 — Smoke Health Economic Cost: $0.5B – $1.0B**
What it measures: Health cost of 14 days PM2.5 exposure to 4.2M residents.
Source: EPA BenMAP COI methodology applied to SmokeStory sensor data.

Full methodology: https://smokestory.onrender.com/methodology
Impact page: https://smokestory.onrender.com/impact

### Data Quality Warnings
- Automatic detection of suspect PM2.5 readings during major fire events (monitor outages)
- Warning displayed when smoke is present but PM2.5 is anomalously low
- Date validation blocks pre-2005 and future dates

---

## Data Sources

| Source | What It Provides | Update Frequency |
|--------|-----------------|-----------------|
| **NASA FIRMS VIIRS** | Active fire detections with FRP | ~3 hours |
| **NOAA HMS** | Smoke plume boundaries (Light/Medium/Heavy) | Daily |
| **EPA AQS (param 88101)** | PM2.5 ground monitor readings | Daily |
| **Guardian API** | News headlines for narrative context | Real-time |
| **CAL FIRE DINS** | Structure damage counts | Static snapshot, Feb 5, 2025 |
| **CAR 2024** | Pre-fire property values | Static 2024 annual data |

PM2.5 standard: Uses revised February 2024 EPA thresholds (Good: 0–9 µg/m³, replacing the previous 0–12 µg/m³ standard).

---

## Architecture

```
smokestory/
├── api/
│   └── main.py                  # FastAPI backend — all HTTP endpoints
│
├── pipeline/
│   ├── epa_aqs.py               # EPA PM2.5 data ingestion
│   ├── goes_hms.py              # NOAA smoke polygon fetching
│   ├── viirs_fire.py            # NASA fire detection fetching
│   ├── build_layer.py           # Spatial join and county data assembly
│   └── news.py                  # Guardian API headlines
│
├── narrative/
│   └── generator.py             # Claude narrative engine
│
├── frontend/
│   ├── index.html               # Main SmokeStory map interface
│   ├── impact.html              # Financial Impact page
│   └── methodology.html         # Full methodology document
│
├── render.yaml                  # Render deployment configuration
├── requirements.txt
└── .env.example
```

**Backend:** FastAPI + Python
**Frontend:** Leaflet.js + Flatpickr (single-file HTML, no build step)
**AI:** Anthropic Claude claude-sonnet-4-20250514
**Deployment:** Render free tier
**Geospatial:** GeoPandas for spatial joins

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Main SmokeStory map |
| `GET` | `/impact` | Financial Impact page |
| `GET` | `/methodology` | Full methodology document |
| `GET` | `/health` | Health check |
| `GET` | `/county/{state}/{county}/{date}` | County data + narrative |
| `GET` | `/top-stories/{date}` | Top 3 CA counties by PM2.5 |
| `GET` | `/map/pm25/06/{date}` | PM2.5 GeoJSON for CA counties |
| `GET` | `/map/smoke/{date}` | HMS smoke polygons GeoJSON |
| `GET` | `/map/fires/{date}` | VIIRS fire points GeoJSON |

Date format: YYYYMMDD (e.g. 20250109)
State code: 06 (California)

---

## Local Development

```bash
git clone https://github.com/tinahuang1994/smokestory.git
cd smokestory

python -m venv venv
source venv/bin/activate        # Mac/Linux

pip install -r requirements.txt

cp .env.example .env            # Add your API keys

uvicorn api.main:app --reload
```

Open http://127.0.0.1:8000 in your browser.

### Required API Keys

| Key | Where to get it |
|-----|----------------|
| `ANTHROPIC_API_KEY` | console.anthropic.com |
| `FIRMS_MAP_KEY` | firms.modaps.eosdis.nasa.gov |
| `EPA_AQS_EMAIL` | aqs.epa.gov data API page |
| `EPA_AQS_KEY` | aqs.epa.gov data API page |
| `GUARDIAN_API_KEY` | open-platform.theguardian.com |

---

## Financial Impact Methodology

The financial impact module uses three independent methodologies — one per estimate:

**Estimate 01 — Direct Destruction ($36B – $40B)**
CAL FIRE DINS structure counts × CAR 2024 pre-fire median prices. Validated against Milliman insured loss estimate of $25.2B–$39.4B.

**Estimate 02 — Neighborhood Value Impact ($3.9B)**
Sathaye et al. 2024, Landscape and Urban Planning. 2.2% average property value decline within 5-mile affected zone applied to $175B surviving housing stock.

**Estimate 03 — Smoke Health Cost ($0.5B – $1.0B)**
EPA BenMAP-CE simplified COI chain applied to SmokeStory PM2.5 sensor data. 14-day exposure period, 4.2M residents, EPA TSD 2023 health impact functions.

Full methodology: https://smokestory.onrender.com/methodology

---

## Key Design Decisions

**Why mean not max for PM2.5?**
We show the daily mean across all monitors in a county rather than the maximum, for consistency between the map visualization and the AI narrative. The tooltip labels this clearly as daily mean.

**Why 2024 EPA thresholds?**
The EPA revised PM2.5 standards in February 2024, lowering the Good/Moderate boundary from 12 to 9 µg/m³. SmokeStory uses current standards.

**Why COI not VSL for health costs?**
Cost of Illness is more appropriate for acute 14-day exposure events. VSL is designed for chronic long-term regulatory analysis and would produce misleadingly large numbers for a short-duration event.

---

## Known Limitations

- EPA monitors are sparse in rural counties — many show No data not because air is clean but because no monitor exists
- HMS smoke polygons show atmospheric smoke — ground-level impact may differ
- PM2.5 data for recent dates may be preliminary (AQS finalizes data 2–6 months after collection)
- Financial impact figures are estimates using public data — not actuarial or academic models
- Fire perimeter boundaries on the impact page are approximate polygons for visualization only

---

## Acknowledgments

Data provided by NASA FIRMS, NOAA HMS, EPA AQS, and The Guardian. AI narratives powered by Anthropic Claude. Built with FastAPI, Leaflet.js, and GeoPandas.

SmokeStory is an independent open-source project. Not affiliated with any government agency, insurance company, or academic institution.

Built by Tina Huang · tina.huang@aya.yale.edu
