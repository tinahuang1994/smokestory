# SmokeStory

**AI-powered wildfire smoke narratives for California's 58 counties**

SmokeStory turns raw environmental data into plain-English stories. Every day, for every county in California, it fuses ground-level air quality readings, satellite smoke imagery, and active fire detections into a single AI-generated narrative — giving journalists, public health researchers, and affected communities the context they need, fast. Navigate to any historic wildfire event back to 2005, click a county, and read the story of the smoke.

---

## What It Does

- **Interactive map** — overlays PM2.5 air quality by county, NOAA satellite smoke plumes, and NASA active fire detections on a single dark-mode Leaflet canvas
- **AI narratives** — click any California county to generate a 4-sentence journalistic narrative powered by Claude, grounded in that day's actual sensor data
- **Historic events** — a curated dropdown of California's most significant wildfire events (Camp Fire, Dixie Fire, Palisades Fire, and more) loads the exact date with one click
- **News integration** — Guardian API headlines from the same date are woven into every narrative and surfaced as source links in the panel

---

## Data Sources

| Source | What It Provides |
|--------|-----------------|
| **EPA Air Quality System (AQS)** | Ground-level PM2.5 daily averages from monitoring stations across California |
| **NOAA Hazard Mapping System (HMS)** | Smoke plume polygons manually analyzed by meteorologists from GOES satellite imagery, classified as Light / Medium / Heavy |
| **NASA VIIRS/FIRMS** | Active fire detections from the Suomi-NPP satellite at 375m resolution, with Fire Radiative Power (FRP) intensity values |
| **The Guardian API** | News headlines from the date being explored, for historical context in AI narratives |
| **US Census TIGER/Line** | County boundary shapefiles (GENZ 2022, 5m resolution) downloaded and cached locally |

---

## Tech Stack

**Backend**
- Python 3.11, FastAPI, Uvicorn
- GeoPandas + Shapely for spatial joins (smoke plumes × county polygons)
- Pandas for PM2.5 aggregation
- Anthropic Claude API (`claude-sonnet-4-20250514`) for narrative generation and chat

**Frontend**
- Vanilla JavaScript — no framework, single HTML file
- [Leaflet.js](https://leafletjs.com/) 1.9.4 — interactive map with GeoJSON layers
- [Flatpickr](https://flatpickr.js.org/) — date picker with historic range back to 2005
- Cormorant Garamond · DM Mono · DM Sans — editorial typography
- CartoDB Dark Matter basemap

---

## Getting Started

### Prerequisites

- Python 3.11+
- API keys for EPA AQS, NASA FIRMS, and Anthropic Claude
- The Guardian API key (optional — defaults to `test` key with limited quota)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/your-username/smokestory.git
cd smokestory
```

**2. Create and activate a virtual environment**
```bash
python3.11 -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**
```bash
cp .env.example .env
# Edit .env and fill in your API keys (see below)
```

**5. Start the API server**
```bash
uvicorn api.main:app --reload
```

The API will be available at `http://localhost:8000`. On first run, county boundary shapefiles (~50 MB) are downloaded from the US Census and cached to `data/counties.geojson`.

**6. Open the frontend**

Open `frontend/index.html` directly in your browser. No build step required.

---

### Environment Variables

Create a `.env` file in the project root with the following keys:

```env
# Required
ANTHROPIC_API_KEY=sk-ant-...          # Claude API key — narratives and chat
FIRMS_MAP_KEY=...                     # NASA FIRMS map key — active fire data
EPA_AQS_EMAIL=you@example.com         # EPA AQS account email
EPA_AQS_KEY=...                       # EPA AQS API key

# Optional
GUARDIAN_API_KEY=...                  # The Guardian API key (defaults to "test")
NEWS_API_KEY=...                      # Reserved for future news source expansion
```

**Getting API keys:**
- **Anthropic**: [console.anthropic.com](https://console.anthropic.com)
- **NASA FIRMS**: [firms.modaps.eosdis.nasa.gov/api](https://firms.modaps.eosdis.nasa.gov/api/map_key/)
- **EPA AQS**: [aqs.epa.gov/aqsweb/documents/data_api.html](https://aqs.epa.gov/aqsweb/documents/data_api.html)
- **The Guardian**: [open-platform.theguardian.com](https://open-platform.theguardian.com/access/)

---

## Project Structure

```
smokestory/
├── api/
│   └── main.py                 # FastAPI app — all HTTP endpoints
│
├── pipeline/
│   ├── build_layer.py          # Assembles county layer (PM2.5 + smoke spatial join)
│   ├── epa_aqs.py              # Fetches PM2.5 readings from EPA AQS API
│   ├── goes_hms.py             # Downloads NOAA HMS smoke plume polygons
│   ├── viirs_fire.py           # Fetches active fire detections from NASA FIRMS
│   └── news.py                 # Queries The Guardian API for headlines
│
├── narrative/
│   ├── generator.py            # Claude-powered narrative generation
│   └── prompts.py              # Prompt templates
│
├── frontend/
│   └── index.html              # Single-file SPA — map, panel, chat UI
│
├── data/                       # Auto-generated on first run
│   └── counties.geojson        # Cached US county boundaries (Census TIGER)
│
├── requirements.txt
├── .env.example
└── README.md
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/county/{state}/{county}/{date}` | County data + AI narrative for a given date |
| `GET` | `/top-stories/{date}` | Top 3 most smoke-affected counties with narratives |
| `GET` | `/map/pm25/06/{date}` | PM2.5 GeoJSON for all California counties |
| `GET` | `/map/smoke/{date}` | NOAA HMS smoke plume GeoJSON |
| `GET` | `/map/fires/{date}` | NASA FIRMS active fire point GeoJSON |
| `GET` | `/news/{county}/{date}` | Guardian headlines for a county and date |
| `POST` | `/chat` | Chat assistant — answers questions grounded in county data |

---

## Open Source

SmokeStory is fully open source. Any city, NGO, newsroom, or researcher can deploy their own instance or adapt the stack for a different environmental hazard — air quality in other states, flood risk, drought severity, or any phenomenon where satellite data meets lived human experience.

Pull requests and forks are welcome.

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Acknowledgments

Built with data from **NOAA**, **NASA**, and the **U.S. Environmental Protection Agency** — all freely available through public APIs. Narratives powered by **Anthropic Claude**. News context from **The Guardian Open Platform**.

> *Wildfire smoke is one of the fastest-growing air quality threats in the American West. SmokeStory exists to make that data legible to the people who need it most.*
